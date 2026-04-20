import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Optional

from measurement import (
    ComponentPath,
    Focus,
    MeasurementQuantity,
    Position,
    Sample,
    Scan,
    Slit,
    Wavelength,
    XRayTube,
    XRDMeasurement,
    XRDMeasurements,
)

__package__ = "a6.parser"


class XRDMLParser:
    """Parses an XRDML XML string or file into typed dataclasses."""

    NAMESPACE = {"xrd": "http://www.xrdml.com/XRDMeasurement/2.1"}

    @classmethod
    def parse_string(cls, xml_string: str) -> XRDMeasurements:
        root = ET.fromstring(xml_string)
        return cls._parse_root(root)

    @classmethod
    def parse_file(cls, filepath: str | Path) -> XRDMeasurements:
        tree = ET.parse(filepath)
        return cls._parse_root(tree.getroot())

    @classmethod
    def _get_text(cls, elem: ET.Element, xpath: str, default: str = "") -> str:
        found = elem.find(xpath, cls.NAMESPACE)
        return found.text if found is not None and found.text is not None else default

    @classmethod
    def _get_float(cls, elem: Optional[ET.Element], xpath: str) -> float:
        text = cls._get_text(elem, xpath)
        return float(text) if text else 0.0

    @classmethod
    def _get_quantity(cls, elem: ET.Element, xpath: str) -> Optional[MeasurementQuantity]:
        if (found := elem.find(xpath, cls.NAMESPACE)) is not None:
            if found.text and found.attrib.get("unit"):
                return MeasurementQuantity(value=float(found.text), unit=found.attrib["unit"])
        return None

    @classmethod
    def _parse_sample(cls, elem: ET.Element) -> Sample:
        return Sample(
            type=elem.attrib.get("type", ""),
            id=cls._get_text(elem, "xrd:id"),
            name=cls._get_text(elem, "xrd:name"),
            prepared_by=cls._get_text(elem, "xrd:preparedBy"),
        )
    
    @classmethod
    def _parse_wavelength(cls, elem: ET.Element) -> Wavelength:
        return Wavelength(
            intended=elem.attrib.get("intended", ""),
            k_alpha_1=cls._get_quantity(elem, "xrd:kAlpha1"),
            k_alpha_2=cls._get_quantity(elem, "xrd:kAlpha2"),
            k_beta=cls._get_quantity(elem, "xrd:kBeta"),
            ratio_k_alpha2_k_alpha1=cls._get_float(elem, "xrd:ratioKAlpha2KAlpha1"),
        )

    @classmethod
    def _parse_root(cls, root: ET.Element) -> XRDMeasurements:

        # get status and comments
        status: str = root.attrib.get("status", "")
        entries = root.findall("xrd:comment/xrd:entry", cls.NAMESPACE)
        comments: list[str] = [entry.text for entry in entries if entry.text]

        # get sample info
        sample_elem = root.find("xrd:sample", cls.NAMESPACE)
        if sample_elem is None:
            raise ValueError("No sample information found in the XRDML file.")
        sample: Sample = cls._parse_sample(sample_elem)

        # get measurement info
        measurement_element = root.find("xrd:xrdMeasurement", cls.NAMESPACE)
        if measurement_element is None:
            raise ValueError("No measurement information found in the XRDML file.")
        measurement: XRDMeasurement = cls._parse_measurement(measurement_element)

        return XRDMeasurements(status=status, comments=comments, sample=sample, measurement=measurement)

    @classmethod
    def _parse_measurement(cls, elem: ET.Element) -> XRDMeasurement:
        entries = elem.findall("xrd:comment/xrd:entry", cls.NAMESPACE)
        comments: list[str] = [entry.text for entry in entries if entry.text]

        # get wavelength info
        wave_elemt = elem.find("xrd:usedWavelength", cls.NAMESPACE)
        if wave_elemt is None:
            raise ValueError("No wavelength information found in the XRDML file.")
        wavelength: Wavelength = cls._parse_wavelength(wave_elemt)

        # get beam path info
        inc_element = elem.find("xrd:incidentBeamPath", cls.NAMESPACE)
        if inc_element is None:
            raise ValueError("No incident beam path information found in the XRDML file.")
        inc_beam_path: ComponentPath = cls._parse_beam_path(inc_element)

        diff_element = elem.find("xrd:diffractedBeamPath", cls.NAMESPACE)
        if diff_element is None:
            raise ValueError("No diffracted beam path information found in the XRDML file.")
        diff_beam_path: ComponentPath = cls._parse_beam_path(diff_element)


        sample_offset = []
        for pos in elem.findall("./xrd:sampleOffset/xrd:position", cls.NAMESPACE):
            sample_offset.append(
                Position(
                    axis=pos.attrib.get("axis", ""),
                    unit=pos.attrib.get("unit", ""),
                    value=float(pos.text) if pos.text else None,
                )
            )

        scan = cls._parse_scan(elem.find("xrd:scan", cls.NAMESPACE))

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
    def _parse_xray_tube(cls, elem: ET.Element) -> XRayTube:
        focus = None
        focus_elem = elem.find("xrd:focus", cls.NAMESPACE)
        if focus_elem is not None:
            focus = Focus(
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
    def _parse_beam_path(cls, elem: ET.Element) -> ComponentPath:

        radius = cls._get_quantity(elem, "xrd:radius")

        tube = None
        tube_elem = elem.find("xrd:xRayTube", cls.NAMESPACE)
        if tube_elem is not None:
            tube: XRayTube = cls._parse_xray_tube(tube_elem)

        soller_elem = elem.find("xrd:sollerSlit", cls.NAMESPACE)
        soller = (
            Slit(
                id=soller_elem.attrib.get("id", ""),
                name=soller_elem.attrib.get("name", ""),
                opening=cls._get_quantity(soller_elem, "xrd:opening"),
            )
            if soller_elem is not None
            else None
        )

        div_elem = elem.find("xrd:divergenceSlit", cls.NAMESPACE)
        divergence = (
            Slit(
                id=div_elem.attrib.get("id", ""),
                name=div_elem.attrib.get("name", ""),
                opening=cls._get_quantity(div_elem, "xrd:opening"),
                distance_to_sample=cls._get_quantity(div_elem, "xrd:distanceToSample"),
                height=cls._get_quantity(div_elem, "xrd:height"),
            )
            if div_elem is not None
            else None
        )

        return ComponentPath(radius=radius, x_ray_tube=tube, soller_slit=soller, divergence_slit=divergence)

    @classmethod
    def _parse_scan(cls, elem: Optional[ET.Element]) -> Optional[Scan]:
        if elem is None:
            return None

        hkl_elem = elem.find("./xrd:reflection/xrd:hkl", cls.NAMESPACE)
        reflection = None
        if hkl_elem is not None:
            reflection = Reflection(
                material=cls._get_text(elem, "./xrd:reflection/xrd:material"),
                miller_h=int(cls._get_text(hkl_elem, "xrd:h", "0")),
                miller_k=int(cls._get_text(hkl_elem, "xrd:k", "0")),
                miller_l=int(cls._get_text(hkl_elem, "xrd:l", "0")),
            )

        dp_elem = elem.find("xrd:dataPoints", cls.NAMESPACE)
        positions = []
        counts = []
        common_time = None

        if dp_elem is not None:
            for pos_elem in dp_elem.findall("xrd:positions", cls.NAMESPACE):
                positions.append(
                    Position(
                        axis=pos_elem.attrib.get("axis", ""),
                        unit=pos_elem.attrib.get("unit", ""),
                        common_position=cls._get_float(pos_elem, "xrd:commonPosition")
                        if pos_elem.find("xrd:commonPosition", cls.NAMESPACE) is not None
                        else None,
                        start_position=cls._get_float(pos_elem, "xrd:startPosition")
                        if pos_elem.find("xrd:startPosition", cls.NAMESPACE) is not None
                        else None,
                        end_position=cls._get_float(pos_elem, "xrd:endPosition")
                        if pos_elem.find("xrd:endPosition", cls.NAMESPACE) is not None
                        else None,
                    )
                )

            counts_text = cls._get_text(dp_elem, "xrd:counts")
            counts = [int(x) for x in counts_text.split()] if counts_text else []
            common_time = cls._get_quantity(dp_elem, "xrd:commonCountingTime")

        data_points = DataPoints(positions=positions, common_counting_time=common_time, counts=counts)

        return Scan(
            mode=elem.attrib.get("mode", ""),
            scan_axis=elem.attrib.get("scanAxis", ""),
            status=elem.attrib.get("status", ""),
            start_time=cls._get_text(elem, "./xrd:header/xrd:startTimeStamp"),
            end_time=cls._get_text(elem, "./xrd:header/xrd:endTimeStamp"),
            center_position=cls._get_float(elem, "./xrd:scanAxisCenter/xrd:position"),
            reflection=reflection,
            data_points=data_points,
        )


measurement = XRDMLParser.parse_file("/home/simon/ProjectsTex/semiconductor_lab/a6/data/Task1_omega_scan_024_al2o3peak_1deg_.005ss_phi=0.xrdml")