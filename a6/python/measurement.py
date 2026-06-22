from dataclasses import dataclass
from typing import List, Optional

from numpy.typing import NDArray

import numpy as np


@dataclass
class MeasurementQuantity:
    value: float
    unit: str


@dataclass
class LatticePlane:
    h: int
    k: int
    l: int


@dataclass
class Position:
    axis: str
    unit: str
    value: Optional[float] = None
    start_position: Optional[float] = None
    end_position: Optional[float] = None
    common_position: Optional[float] = None


@dataclass
class Focus:
    type: str
    length: MeasurementQuantity
    width: MeasurementQuantity
    take_off_angle: MeasurementQuantity


@dataclass
class Crystal:
    material: str
    type: str
    shape: str


@dataclass
class XRayTube:
    id: str
    name: str
    anode_material: str
    tension: MeasurementQuantity
    current: MeasurementQuantity
    focus: Optional[Focus]


@dataclass
class XRayMirror:
    id: str
    name: str
    hybrid: bool
    crystal: Crystal
    acceptance_angle: MeasurementQuantity
    length: MeasurementQuantity


@dataclass
class Monochromator:
    id: str
    name: str
    hybrid: bool
    crystal: Crystal
    reflection_number: int
    lattice_plane: LatticePlane


@dataclass
class Slit:
    id: str
    name: str
    type: Optional[str]
    opening: Optional[MeasurementQuantity]
    distance_to_sample: Optional[MeasurementQuantity]
    height: Optional[MeasurementQuantity]


@dataclass
class Detector:
    id: str
    name: str
    type: str
    phd_lower: MeasurementQuantity
    phd_upper: MeasurementQuantity
    mode: str
    active_channel_equatorial: str
    active_channel_axial: str
    pitch_equatorial: MeasurementQuantity
    pitch_axial: MeasurementQuantity
    read_out_period: MeasurementQuantity


@dataclass
class Wavelength:
    intended: Optional[str]
    k_alpha_1: Optional[MeasurementQuantity]
    k_alpha_2: Optional[MeasurementQuantity]
    k_beta: Optional[MeasurementQuantity]
    ratio_k_alpha2_k_alpha1: Optional[float]


@dataclass
class ComponentPath:
    radius: Optional[MeasurementQuantity]
    x_ray_tube: Optional[XRayTube]
    x_ray_mirror: Optional[XRayMirror]
    monochromator: Optional[Monochromator]
    soller_slit: Optional[Slit]
    divergence_slit: Optional[Slit]
    detector: Optional[Detector]


@dataclass
class Scan:
    mode: str
    scan_axis: str
    status: str
    start_time: str
    end_time: str
    center_position: Position
    material: str
    lattice_plane: LatticePlane
    positions: list[Position]
    common_counting_time: MeasurementQuantity
    counts: List[int]
    counts_unit: str

    def get_plot_data(self) -> dict[str, NDArray[np.float64]]:
        start_position: Optional[float] = None
        end_position: Optional[float] = None

        plot_data: dict[str, NDArray[np.float64]] = {}
        for position in self.positions:
            if position.start_position is not None and position.end_position is not None:
                start_position = position.start_position
                end_position = position.end_position
                name = str(position.axis).lower()
                plot_data[name] = np.linspace(start_position, end_position, num=len(self.counts))


        plot_data["intensity"] = np.array([float(count) for count in self.counts])
        return plot_data

    def get_position(self, axis: str) -> float:
        for position in self.positions:
            if position.axis == axis and position.common_position:
                return position.common_position
        raise ValueError("axis value not found")


@dataclass
class Sample:
    type: Optional[str]
    id: Optional[str]
    name: Optional[str]
    prepared_by: Optional[str]


@dataclass
class XRDMeasurement:
    scan: Scan
    measurement_type: str
    status: str
    sample_mode: str
    comments: List[str]
    used_wavelength: Wavelength
    incident_beam_path: ComponentPath
    sample_offset: List[Position]
    diffracted_beam_path: ComponentPath


@dataclass
class XRDSession:
    status: str
    comments: List[str]
    sample: Sample
    measurement: XRDMeasurement
