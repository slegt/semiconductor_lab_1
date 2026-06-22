import xml.etree.ElementTree as ET

from xml.etree.ElementTree import Element
from pathlib import Path
from typing import Optional

from measurement import (
    ComponentPath,
    Crystal,
    Detector,
    Focus,
    LatticePlane,
    MeasurementQuantity,
    Monochromator,
    Position,
    Sample,
    Scan,
    Slit,
    Wavelength,
    XRayMirror,
    XRayTube,
    XRDMeasurement,
    XRDSession,
)

__package__ = "a6.parser"


class XRDMLParser:
    """Parses an XRDML XML string or file into typed dataclasses."""

    NAMESPACE = {"xrd": "http://www.xrdml.com/XRDMeasurement/2.1"}

    @classmethod
    def parse_string(cls, xml_string: str) -> XRDSession:
        root = ET.fromstring(xml_string)
        return cls._parse_root(root)

    @classmethod
    def parse_file(cls, filepath: str | Path) -> XRDSession:
        tree = ET.parse(filepath)
        return cls._parse_root(tree.getroot())

    @classmethod
    def _get_text(cls, elem: Element, xpath: str) -> str:
        found = elem.find(xpath, cls.NAMESPACE)
        if found is None or found.text is None:
            raise ValueError(f"Expected text at '{xpath}' not found in the XRDML file.")
        return found.text

    @classmethod
    def _get_optional_text(cls, elem: Element, xpath: str) -> Optional[str]:
        found = elem.find(xpath, cls.NAMESPACE)
        return found.text if found is not None and found.text else None

    @classmethod
    def _get_float(cls, elem: Element, xpath: str) -> float:
        text = cls._get_text(elem, xpath)
        try:
            return float(text)
        except ValueError:
            raise ValueError(f"Expected float at '{xpath}' but got '{text}' in the XRDML file.")

    @classmethod
    def _get_optional_float(cls, elem: Element, xpath: str) -> Optional[float]:
        text = cls._get_optional_text(elem, xpath)
        return float(text) if text else None

    @classmethod
    def _get_int(cls, elem: Element, xpath: str) -> int:
        text = cls._get_text(elem, xpath)
        try:
            return int(text)
        except ValueError:
            raise ValueError(f"Expected int at '{xpath}' but got '{text}' in the XRDML file.")

    @classmethod
    def _get_optional_int(cls, elem: Element, xpath: str) -> Optional[int]:
        text = cls._get_text(elem, xpath)
        return int(text) if text else None

    @classmethod
    def _get_quantity(cls, elem: Element, xpath: str) -> MeasurementQuantity:
        if (found := elem.find(xpath, cls.NAMESPACE)) is not None:
            if found.text and found.attrib.get("unit"):
                return MeasurementQuantity(value=float(found.text), unit=found.attrib["unit"])
        raise ValueError(f"Expected quantity at '{xpath}' not found in the XRDML file.")

    @classmethod
    def _get_optional_quantity(cls, elem: Element, xpath: str) -> Optional[MeasurementQuantity]:
        try:
            return cls._get_quantity(elem, xpath)
        except ValueError:
            return None

    @classmethod
    def _parse_sample(cls, elem: Element) -> Sample:
        return Sample(
            type=elem.attrib.get("type"),
            id=cls._get_optional_text(elem, "xrd:id"),
            name=cls._get_optional_text(elem, "xrd:name"),
            prepared_by=cls._get_optional_text(elem, "xrd:preparedBy"),
        )

    @classmethod
    def _parse_wavelength(cls, elem: Element) -> Wavelength:
        return Wavelength(
            intended=elem.attrib.get("intended", ""),
            k_alpha_1=cls._get_quantity(elem, "xrd:kAlpha1"),
            k_alpha_2=cls._get_quantity(elem, "xrd:kAlpha2"),
            k_beta=cls._get_quantity(elem, "xrd:kBeta"),
            ratio_k_alpha2_k_alpha1=cls._get_float(elem, "xrd:ratioKAlpha2KAlpha1"),
        )

    @classmethod
    def _parse_root(cls, root: Element) -> XRDSession:

        # get status and comments
        status: str = root.attrib.get("status", "")
        entries: list[Element] = root.findall("xrd:comment/xrd:entry", cls.NAMESPACE)
        comments: list[str] = [entry.text for entry in entries if entry.text]

        # get sample info
        sample_elem: Optional[Element] = root.find("xrd:sample", cls.NAMESPACE)
        if sample_elem is None:
            raise ValueError("No sample information found in the XRDML file.")
        sample: Sample = cls._parse_sample(sample_elem)

        # get measurement info
        measurement_element: Optional[Element] = root.find("xrd:xrdMeasurement", cls.NAMESPACE)
        if measurement_element is None:
            raise ValueError("No measurement information found in the XRDML file.")
        measurement: XRDMeasurement = cls._parse_measurement(measurement_element)

        return XRDSession(status=status, comments=comments, sample=sample, measurement=measurement)

    @classmethod
    def _parse_measurement(cls, elem: Element) -> XRDMeasurement:
        entries = elem.findall("xrd:comment/xrd:entry", cls.NAMESPACE)
        comments: list[str] = [entry.text for entry in entries if entry.text]

        # get wavelength info
        wave_elemt: Optional[Element] = elem.find("xrd:usedWavelength", cls.NAMESPACE)
        if wave_elemt is None:
            raise ValueError("No wavelength information found in the XRDML file.")
        wavelength: Wavelength = cls._parse_wavelength(wave_elemt)

        # get beam path info
        inc_element: Optional[Element] = elem.find("xrd:incidentBeamPath", cls.NAMESPACE)
        if inc_element is None:
            raise ValueError("No incident beam path information found in the XRDML file.")
        inc_beam_path: ComponentPath = cls._parse_beam_path(inc_element)

        diff_element: Optional[Element] = elem.find("xrd:diffractedBeamPath", cls.NAMESPACE)
        if diff_element is None:
            raise ValueError("No diffracted beam path information found in the XRDML file.")
        diff_beam_path: ComponentPath = cls._parse_beam_path(diff_element)

        sample_offset = []
        pos_elems: list[Element] = elem.findall("./xrd:sampleOffset/xrd:position", cls.NAMESPACE)
        for pos in pos_elems:
            sample_offset.append(
                Position(
                    axis=pos.attrib.get("axis", ""), unit=pos.attrib.get("unit", ""), value=cls._get_float(pos, ".")
                )
            )

        scan_elem = elem.find("xrd:scan", cls.NAMESPACE)
        if scan_elem is None:
            raise ValueError("No scan information found in the XRDML file.")
        scan: Scan = cls._parse_scan(scan_elem)

        return XRDMeasurement(
            measurement_type=elem.attrib.get("measurementType", ""),
            status=elem.attrib.get("status", ""),
            sample_mode=elem.attrib.get("sampleMode", ""),
            comments=comments,
            used_wavelength=wavelength,
            incident_beam_path=inc_beam_path,
            sample_offset=sample_offset,
            diffracted_beam_path=diff_beam_path,
            scan=scan,
        )

    @classmethod
    def _parse_xray_tube(cls, elem: Element) -> XRayTube:
        focus_elem: Optional[Element] = elem.find("xrd:focus", cls.NAMESPACE)
        if focus_elem is None:
            raise ValueError("X-ray tube focus information is missing in the XRDML file.")
        focus: Focus = Focus(
            type=focus_elem.attrib.get("type", ""),
            length=cls._get_quantity(focus_elem, "xrd:length"),
            width=cls._get_quantity(focus_elem, "xrd:width"),
            take_off_angle=cls._get_quantity(focus_elem, "xrd:takeOffAngle"),
        )
        return XRayTube(
            id=elem.attrib.get("id", ""),
            name=elem.attrib.get("name", ""),
            tension=cls._get_quantity(elem, "xrd:tension"),
            current=cls._get_quantity(elem, "xrd:current"),
            anode_material=cls._get_text(elem, "xrd:anodeMaterial"),
            focus=focus,
        )

    @classmethod
    def _parse_xray_mirror(cls, elem: Element) -> XRayMirror:
        crystal_elem: Optional[Element] = elem.find("xrd:crystal", cls.NAMESPACE)
        if crystal_elem is None:
            raise ValueError("X-ray mirror crystal information is missing in the XRDML file.")
        crystal: Crystal = Crystal(
            material=cls._get_text(elem, "xrd:crystal"),
            type=crystal_elem.attrib.get("type", ""),
            shape=crystal_elem.attrib.get("shape", ""),
        )

        return XRayMirror(
            id=elem.attrib.get("id", ""),
            name=elem.attrib.get("name", ""),
            hybrid=bool(elem.attrib.get("hybrid", "false").lower() == "true"),
            acceptance_angle=cls._get_quantity(elem, "xrd:acceptanceAngle"),
            length=cls._get_quantity(elem, "xrd:length"),
            crystal=crystal,
        )

    @classmethod
    def _parse_monochromator(cls, elem: Element) -> Monochromator:
        crystal_elem: Optional[Element] = elem.find("xrd:crystal", cls.NAMESPACE)
        if crystal_elem is None:
            raise ValueError("X-ray mirror crystal information is missing in the XRDML file.")
        crystal: Crystal = Crystal(
            material=cls._get_text(elem, "xrd:crystal"),
            type=crystal_elem.attrib.get("type", ""),
            shape=crystal_elem.attrib.get("shape", ""),
        )

        return Monochromator(
            id=elem.attrib.get("id", ""),
            name=elem.attrib.get("name", ""),
            hybrid=bool(elem.attrib.get("hybrid", "false").lower() == "true"),
            crystal=crystal,
            reflection_number=cls._get_int(elem, "xrd:numberOfReflections"),
            lattice_plane=LatticePlane(
                h=cls._get_int(elem, "xrd:hkl/xrd:h"),
                k=cls._get_int(elem, "xrd:hkl/xrd:k"),
                l=cls._get_int(elem, "xrd:hkl/xrd:l"),
            ),
        )

    @classmethod
    def _parse_detector(cls, elem: Element) -> Detector:
        phd_elem = elem.find("xrd:phd", cls.NAMESPACE)
        if phd_elem is None:
            raise ValueError("Detector PHD information is missing in the XRDML file.")

        phd_unit = phd_elem.attrib.get("unit", "")
        phd_lower_elem = phd_elem.find("xrd:lowerLevel", cls.NAMESPACE)
        phd_upper_elem = phd_elem.find("xrd:upperLevel", cls.NAMESPACE)
        if phd_lower_elem is None or phd_lower_elem.text is None:
            raise ValueError("Detector lower PHD level is missing in the XRDML file.")
        if phd_upper_elem is None or phd_upper_elem.text is None:
            raise ValueError("Detector upper PHD level is missing in the XRDML file.")

        return Detector(
            id=elem.attrib.get("id", ""),
            name=elem.attrib.get("name", ""),
            type=elem.attrib.get("xsi:type", ""),
            phd_lower=MeasurementQuantity(value=float(phd_lower_elem.text), unit=phd_unit),
            phd_upper=MeasurementQuantity(value=float(phd_upper_elem.text), unit=phd_unit),
            mode=cls._get_text(elem, "xrd:mode"),
            active_channel_equatorial=cls._get_text(elem, "xrd:activeChannelsEquatorial"),
            active_channel_axial=cls._get_text(elem, "xrd:activeChannelsAxial"),
            pitch_equatorial=cls._get_quantity(elem, "xrd:pitchEquatorial"),
            pitch_axial=cls._get_quantity(elem, "xrd:pitchAxial"),
            read_out_period=cls._get_quantity(elem, "xrd:readOutPeriod"),
        )

    @classmethod
    def _parse_beam_path(cls, elem: Element) -> ComponentPath:

        radius = cls._get_quantity(elem, "xrd:radius")

        tube: Optional[XRayTube] = None
        tube_elem: Optional[Element] = elem.find("xrd:xRayTube", cls.NAMESPACE)
        if tube_elem is not None:
            tube = cls._parse_xray_tube(tube_elem)

        mirror: Optional[XRayMirror] = None
        mirror_elem: Optional[Element] = elem.find("xrd:xRayMirror", cls.NAMESPACE)
        if mirror_elem is not None:
            mirror = cls._parse_xray_mirror(mirror_elem)

        monochromator: Optional[Monochromator] = None
        monochromator_elem = elem.find("xrd:monochromator", cls.NAMESPACE)
        if monochromator_elem is not None:
            monochromator = cls._parse_monochromator(monochromator_elem)

        soller: Optional[Slit] = None
        soller_elem: Optional[Element] = elem.find("xrd:sollerSlit", cls.NAMESPACE)
        if soller_elem is not None:
            soller = Slit(
                id=soller_elem.attrib.get("id", ""),
                name=soller_elem.attrib.get("name", ""),
                type=soller_elem.attrib.get("xsi:type"),
                opening=cls._get_optional_quantity(soller_elem, "xrd:opening"),
                distance_to_sample=cls._get_optional_quantity(soller_elem, "xrd:distanceToSample"),
                height=cls._get_optional_quantity(soller_elem, "xrd:height"),
            )

        divergence: Optional[Slit] = None
        div_elem: Optional[Element] = elem.find("xrd:divergenceSlit", cls.NAMESPACE)
        if div_elem is not None:
            divergence = Slit(
                id=div_elem.attrib.get("id", ""),
                name=div_elem.attrib.get("name", ""),
                type=div_elem.attrib.get("xsi:type"),
                opening=cls._get_optional_quantity(div_elem, "xrd:opening"),
                distance_to_sample=cls._get_optional_quantity(div_elem, "xrd:distanceToSample"),
                height=cls._get_optional_quantity(div_elem, "xrd:height"),
            )

        detector: Optional[Detector] = None
        det_elem: Optional[Element] = elem.find("xrd:detector", cls.NAMESPACE)
        if det_elem is not None:
            detector = cls._parse_detector(det_elem)

        return ComponentPath(
            radius=radius,
            x_ray_tube=tube,
            x_ray_mirror=mirror,
            monochromator=monochromator,
            soller_slit=soller,
            divergence_slit=divergence,
            detector=detector,
        )

    @classmethod
    def _parse_scan(cls, elem: Element) -> Scan:

        header_elem: Optional[Element] = elem.find("xrd:header", cls.NAMESPACE)
        if header_elem is None:
            raise ValueError("Scan header information is missing in the XRDML file.")

        starting_time_elem: Optional[Element] = header_elem.find("xrd:startTimeStamp", cls.NAMESPACE)
        if starting_time_elem is None or starting_time_elem.text is None:
            raise ValueError("Scan start time information is missing in the XRDML file.")
        strating_time: str = starting_time_elem.text

        end_time_elem: Optional[Element] = header_elem.find("xrd:endTimeStamp", cls.NAMESPACE)
        if end_time_elem is None or end_time_elem.text is None:
            raise ValueError("Scan end time information is missing in the XRDML file.")
        end_time: str = end_time_elem.text

        center_pos_elem: Optional[Element] = elem.find("xrd:scanAxisCenter", cls.NAMESPACE)
        if center_pos_elem is None:
            raise ValueError("Scan center position information is missing in the XRDML file.")
        center_position: Position = Position(
            axis=center_pos_elem.attrib.get("axis", ""),
            unit=center_pos_elem.attrib.get("unit", ""),
            value=cls._get_float(center_pos_elem, "xrd:position"),
        )

        material_elem: Optional[Element] = elem.find("./xrd:reflection/xrd:material", cls.NAMESPACE)
        if material_elem is None or material_elem.text is None:
            raise ValueError("Scan reflection material information is missing in the XRDML file.")
        material: str = material_elem.text

        hkl_elem: Optional[Element] = elem.find("./xrd:reflection/xrd:hkl", cls.NAMESPACE)
        if hkl_elem is None:
            raise ValueError("Scan reflection information is missing in the XRDML file.")

        lattice_plane = LatticePlane(
            h=cls._get_int(hkl_elem, "xrd:h"),
            k=cls._get_int(hkl_elem, "xrd:k"),
            l=cls._get_int(hkl_elem, "xrd:l"),
        )

        dp_elem: Optional[Element] = elem.find("xrd:dataPoints", cls.NAMESPACE)
        if dp_elem is None:
            raise ValueError("Scan data points information is missing in the XRDML file.")

        positions: list[Position] = []
        for position_elem in elem.findall("xrd:dataPoints/xrd:positions", cls.NAMESPACE):
            position = Position(
                axis=position_elem.attrib.get("axis", ""),
                unit=position_elem.attrib.get("unit", ""),
                common_position=cls._get_optional_float(position_elem, "xrd:commonPosition"),
                start_position=cls._get_optional_float(position_elem, "xrd:startPosition"),
                end_position=cls._get_optional_float(position_elem, "xrd:endPosition"),
            )
            positions.append(position)

        counts_elem: Optional[Element] = dp_elem.find("xrd:counts", cls.NAMESPACE)
        if counts_elem is None or counts_elem.text is None:
            raise ValueError("Scan counts information is missing in the XRDML file.")

        counts_text: str = cls._get_text(dp_elem, "xrd:counts")
        counts: list[int] = [int(x) for x in counts_text.split()] if counts_text else []
        common_time = cls._get_quantity(dp_elem, "xrd:commonCountingTime")

        return Scan(
            mode=elem.attrib.get("mode", ""),
            scan_axis=elem.attrib.get("scanAxis", ""),
            status=elem.attrib.get("status", ""),
            start_time=strating_time,
            end_time=end_time,
            center_position=center_position,
            material=material,
            lattice_plane=lattice_plane,
            positions=positions,
            common_counting_time=common_time,
            counts=counts,
            counts_unit=counts_elem.attrib.get("unit", ""),
        )
