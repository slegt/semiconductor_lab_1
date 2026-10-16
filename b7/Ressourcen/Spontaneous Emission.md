---
dateCreated: 2026-09-29 17:27
quality: 3
topic: Semiconductors
type: zettel
---

![[Drawing 2026-09-22 18.02.04.excalidraw|200]]

Without any incoming photon, an electron in the conduction band can recombine radiatively with a hole in the valence band. The emitted photons have random directions and phases, so the resulting light is incoherent.

## Spontaneous Emission Line Shape

Following from the general formula in [[Emission and Absorption Rates]], the spontaneous emission rate can be expressed using the equilibrium [[Absorption Coefficient]], the [[Photon Density of States]] and the occupation probabilities, see [[Quasi Fermi Level]].

$$
R^{\mathrm{spon}}(\hbar \omega)=N(\hbar\omega) \frac{c}{n_{\mathrm{r}}} \alpha_{0}(\hbar \omega) f_{\mathrm{n}}f_{\mathrm{p}}
$$

> [!quote]- Symbols
>
> | Symbol | Meaning | Unit |
> |---|---|---|
> | $R^{\mathrm{spon}}$ | spontaneous emission rate, per volume and photon energy | $\mathrm{m^{-3}\,s^{-1}\,J^{-1}}$ |
> | $\hbar\omega$ | photon energy | $\mathrm{J}$ (often eV) |
> | $N(\hbar\omega)$ | photon mode density of states, see [[Photon Density of States]] | $\mathrm{m^{-3}\,J^{-1}}$ |
> | $c$ | speed of light in vacuum | $\mathrm{m\,s^{-1}}$ |
> | $n_{\mathrm{r}}$ | refractive index | dimensionless |
> | $\alpha_0$ | equilibrium absorption coefficient, see [[Absorption Coefficient]] | $\mathrm{m^{-1}}$ |
> | $f_{\mathrm{n}}, f_{\mathrm{p}}$ | probability that a conduction-band state is occupied by an electron / a valence-band state by a hole | dimensionless |

The occupation factors are evaluated in the Boltzmann approximation:

$$
\begin{align}
f_{\mathrm{n}}(E)&=\frac{1}{1+\exp\left( \frac{E-F_{\mathrm{n}}}{k_{\mathrm B}T} \right)} \simeq \exp\left( \frac{F_{\mathrm{n}}-E}{k_{\mathrm B}T} \right) \\
f_{\mathrm{p}}(E)&=\frac{1}{1+\exp\left( \frac{F_{\mathrm{p}}-E}{k_{\mathrm B}T} \right)} \simeq \exp\left( \frac{E-F_{\mathrm{p}}}{k_{\mathrm B}T} \right)
\end{align}
$$

> [!quote]- Symbols
>
> | Symbol | Meaning | Unit |
> |---|---|---|
> | $f_{\mathrm{n}}(E), f_{\mathrm{p}}(E)$ | probability that a conduction-band state is occupied by an electron / a valence-band state by a hole, at energy $E$ | dimensionless |
> | $E$ | energy of the electronic state | $\mathrm{J}$ (often eV) |
> | $F_{\mathrm{n}}, F_{\mathrm{p}}$ | quasi-Fermi levels of electrons/holes | $\mathrm{J}$ (often eV) |
> | $k_{\mathrm B}$ | Boltzmann constant | $\mathrm{J\,K^{-1}}$ |
> | $T$ | temperature | $\mathrm{K}$ |

The factors $f_{\mathrm{n}}$ and $f_{\mathrm{p}}$ are evaluated at the band energies $E_{\mathrm c}(k_0)$ and $E_{\mathrm v}(k_0)$ of the transition, the $\delta$-function fixes their difference to $E_{\mathrm c}(k_0)-E_{\mathrm v}(k_0)=\hbar\omega$. The individual band energies therefore drop out of the product and only the quasi-Fermi-level splitting $\Delta F=F_{\mathrm{n}}-F_{\mathrm{p}}$ and the photon energy remain:

$$
\begin{align}
f_{\mathrm{n}}f_{\mathrm{p}} &\simeq \exp \left( \frac{F_{\mathrm{n}}-F_{\mathrm{p}}-\left(E_{\mathrm c}(k_0)-E_{\mathrm v}(k_0)\right)}{k_{\mathrm B}T} \right)=\exp \left( \frac{\Delta F -\hbar \omega}{k_{\mathrm B}T} \right) \\
&=\exp\left( \frac{\Delta F-E_{\mathrm{g}}}{k_{\mathrm B}T} \right) \exp\left( -\frac{\hbar \omega-E_{\mathrm{g}}}{k_{\mathrm B}T} \right)
\end{align}
$$

> [!quote]- Symbols
>
> | Symbol | Meaning | Unit |
> |---|---|---|
> | $f_{\mathrm{n}}, f_{\mathrm{p}}$ | probability that a conduction-band state is occupied by an electron / a valence-band state by a hole | dimensionless |
> | $F_{\mathrm{n}}, F_{\mathrm{p}}$ | quasi-Fermi levels of electrons/holes | $\mathrm{J}$ (often eV) |
> | $\Delta F$ | quasi-Fermi-level splitting, $\Delta F=F_{\mathrm{n}}-F_{\mathrm{p}}$ | $\mathrm{J}$ (often eV) |
> | $E_{\mathrm c}(k_0), E_{\mathrm v}(k_0)$ | conduction-/valence-band energy at the transition wavevector $k_0$ | $\mathrm{J}$ (often eV) |
> | $\hbar\omega$ | photon energy | $\mathrm{J}$ (often eV) |
> | $E_{\mathrm g}$ | band gap energy | $\mathrm{J}$ (often eV) |
> | $k_{\mathrm B}$ | Boltzmann constant | $\mathrm{J\,K^{-1}}$ |
> | $T$ | temperature | $\mathrm{K}$ |

Inserting this into the rate gives the analytical spontaneous emission spectrum (for $\hbar\omega>E_{\mathrm g}$), where $\Delta F$ only enters the amplitude:

$$
R^{\mathrm{spon}}(\hbar \omega)= N(\hbar\omega)\frac{c}{n_{\mathrm{r}}}\,\alpha_{0}(\hbar \omega)\,\exp\left( \frac{\Delta F-E_{\mathrm{g}}}{k_{\mathrm B}T} \right) \exp\left( -\frac{\hbar \omega-E_{\mathrm{g}}}{k_{\mathrm B}T} \right)
$$

> [!quote]- Symbols
>
> | Symbol | Meaning | Unit |
> |---|---|---|
> | $R^{\mathrm{spon}}$ | spontaneous emission rate, per volume and photon energy | $\mathrm{m^{-3}\,s^{-1}\,J^{-1}}$ |
> | $N(\hbar\omega)$ | photon mode density of states | $\mathrm{m^{-3}\,J^{-1}}$ |
> | $c$ | speed of light in vacuum | $\mathrm{m\,s^{-1}}$ |
> | $n_{\mathrm{r}}$ | refractive index | dimensionless |
> | $\alpha_0$ | equilibrium absorption coefficient | $\mathrm{m^{-1}}$ |
> | $\Delta F$ | quasi-Fermi-level splitting, $\Delta F=F_{\mathrm{n}}-F_{\mathrm{p}}$ | $\mathrm{J}$ (often eV) |
> | $E_{\mathrm g}$ | band gap energy | $\mathrm{J}$ (often eV) |
> | $\hbar\omega$ | photon energy | $\mathrm{J}$ (often eV) |
> | $k_{\mathrm B}$ | Boltzmann constant | $\mathrm{J\,K^{-1}}$ |
> | $T$ | temperature | $\mathrm{K}$ |

With $N\propto(\hbar\omega)^2$ and $\alpha_0\propto\sqrt{\hbar\omega-E_{\mathrm g}}\,/\,\hbar\omega$, the spectral shape follows:

$$
R^{\mathrm{spon}}(\hbar \omega)\propto \hbar\omega\,\sqrt{\hbar\omega-E_{\mathrm g}}\,\exp\left( -\frac{\hbar \omega-E_{\mathrm{g}}}{k_{\mathrm B}T} \right)
$$

> [!quote]- Symbols
>
> | Symbol | Meaning | Unit |
> |---|---|---|
> | $R^{\mathrm{spon}}$ | spontaneous emission rate, per volume and photon energy | $\mathrm{m^{-3}\,s^{-1}\,J^{-1}}$ |
> | $\hbar\omega$ | photon energy | $\mathrm{J}$ (often eV) |
> | $E_{\mathrm g}$ | band gap energy | $\mathrm{J}$ (often eV) |
> | $k_{\mathrm B}$ | Boltzmann constant | $\mathrm{J\,K^{-1}}$ |
> | $T$ | temperature | $\mathrm{K}$ |

## Measurable Quantities

The number of photons emitted per volume and time with photon energies $E=\hbar\omega$ between $E_1$ and $E_2$ is:

$$
N(E_{1}, E_{2}) = \int_{E_1}^{E_2} R^{\mathrm{spon}}(E) \, \mathrm{d}E
$$

> [!quote]- Symbols
>
> | Symbol | Meaning | Unit |
> |---|---|---|
> | $R^{\mathrm{spon}}$ | spontaneous emission rate, per volume and photon energy | $\mathrm{m^{-3}\,s^{-1}\,J^{-1}}$ |
> | $N(E_1, E_2)$ | number of emitted photons per volume and time in the interval $[E_1, E_2]$ | $\mathrm{m^{-3}\,s^{-1}}$ |
> | $E_1, E_2$ | lower/upper photon energy of the interval | $\mathrm{J}$ (often eV) |
> | $E$ | photon energy, $E=\hbar\omega$ | $\mathrm{J}$ (often eV) |

Weighting each photon by its energy gives the spectral power density $p_{E}(E)=E\,R^{\mathrm{spon}}(E)$ and the emitted optical power per volume:

$$
P(E_{1}, E_{2})=\int_{E_1}^{E_2} p_{E}(E) \, \mathrm{d}E = \int_{E_1}^{E_2} E \, R^{\mathrm{spon}}(E) \, \mathrm{d}E
$$

> [!quote]- Symbols
>
> | Symbol | Meaning | Unit |
> |---|---|---|
> | $P(E_1, E_2)$ | emitted optical power per volume in the interval $[E_1, E_2]$ | $\mathrm{W\,m^{-3}}$ |
> | $p_{E}(E)$ | spectral power density of the spontaneous emission | $\mathrm{W\,m^{-3}\,J^{-1}}$ |
> | $E_1, E_2$ | lower/upper photon energy of the interval | $\mathrm{J}$ (often eV) |
> | $E$ | photon energy, $E=\hbar\omega$ | $\mathrm{J}$ (often eV) |
> | $R^{\mathrm{spon}}$ | spontaneous emission rate, per volume and photon energy | $\mathrm{m^{-3}\,s^{-1}\,J^{-1}}$ |

The extra factor $E$ turns the factor $\hbar\omega$ of the rate into $(\hbar\omega)^2$ in the power spectrum:

$$
p_{E}(E)\propto (\hbar\omega)^{2} \sqrt{ \hbar \omega-E_{\mathrm{g}} } \exp\left( -\frac{\hbar \omega-E_{\mathrm{g}}}{k_{\mathrm B}T} \right)
$$

> [!quote]- Symbols
>
> | Symbol | Meaning | Unit |
> |---|---|---|
> | $p_{E}(E)$ | spectral power density of the spontaneous emission | $\mathrm{W\,m^{-3}\,J^{-1}}$ |
> | $E$ | photon energy, $E=\hbar\omega$ | $\mathrm{J}$ (often eV) |
> | $\hbar\omega$ | photon energy | $\mathrm{J}$ (often eV) |
> | $E_{\mathrm g}$ | band gap energy | $\mathrm{J}$ (often eV) |
> | $k_{\mathrm B}$ | Boltzmann constant | $\mathrm{J\,K^{-1}}$ |
> | $T$ | temperature | $\mathrm{K}$ |

Spectrometers usually resolve the emission in wavelength rather than in energy. With $E=hc/\lambda$ (vacuum wavelength $\lambda$), the integral transforms as:

$$
\begin{align}
P(\lambda_{1}, \lambda_{2})&=\int_{E_1}^{E_2} p_{E}(E)\,\mathrm{d}E=\int_{\lambda_2}^{\lambda_1} \underbrace{p_{E}\!\left(\frac{hc}{\lambda}\right)\frac{hc}{\lambda^{2}}}_{p_{\lambda}(\lambda)}\,\mathrm{d}\lambda
\\
\Rightarrow\quad
p_{\lambda}(\lambda)&=p_{E}\!\left(\frac{hc}{\lambda}\right)\frac{hc}{\lambda^{2}}\propto\frac{1}{\lambda^{4}}\sqrt{\frac{hc}{\lambda}-E_{\mathrm{g}}}\,\exp\left( -\frac{\frac{hc}{\lambda}-E_{\mathrm{g}}}{k_{\mathrm B}T} \right)
\end{align}
$$

> [!quote]- Symbols
>
> | Symbol | Meaning | Unit |
> |---|---|---|
> | $P(\lambda_1, \lambda_2)$ | emitted optical power per volume in the interval $[\lambda_2, \lambda_1]$, equal to $P(E_1, E_2)$ | $\mathrm{W\,m^{-3}}$ |
> | $p_{E}(E)$ | spectral power density per photon energy | $\mathrm{W\,m^{-3}\,J^{-1}}$ |
> | $p_{\lambda}(\lambda)$ | spectral power density per wavelength | $\mathrm{W\,m^{-4}}$ |
> | $E_1, E_2$ | lower/upper photon energy of the interval | $\mathrm{J}$ (often eV) |
> | $E$ | photon energy, $E=hc/\lambda$ | $\mathrm{J}$ (often eV) |
> | $\lambda_1, \lambda_2$ | wavelength limits of the interval, $\lambda_{i}=hc/E_{i}$, hence $\lambda_1>\lambda_2$ | $\mathrm{m}$ |
> | $\lambda$ | vacuum wavelength | $\mathrm{m}$ |
> | $h$ | Planck constant | $\mathrm{J\,s}$ |
> | $c$ | speed of light in vacuum | $\mathrm{m\,s^{-1}}$ |
> | $E_{\mathrm g}$ | band gap energy | $\mathrm{J}$ (often eV) |
> | $k_{\mathrm B}$ | Boltzmann constant | $\mathrm{J\,K^{-1}}$ |
> | $T$ | temperature | $\mathrm{K}$ |

A real detector measures the power within a finite bandwidth $\Delta\lambda=\lambda_1-\lambda_2$. If $p_{\lambda}(\lambda)$ varies only slightly within this interval, the integral can be approximated by the midpoint rule, and the spectral power density at the center wavelength $\lambda_{\mathrm c}=(\lambda_1+\lambda_2)/2$ is approximately the measured power divided by the interval width:

$$
P(\lambda_1,\lambda_2)\approx p_{\lambda}(\lambda_{\mathrm c})\,\Delta\lambda
\quad\Rightarrow\quad
p_{\lambda}(\lambda_{\mathrm c})\approx\frac{P(\lambda_1,\lambda_2)}{\Delta\lambda}
$$

> [!quote]- Symbols
>
> | Symbol | Meaning | Unit |
> |---|---|---|
> | $P(\lambda_1,\lambda_2)$ | emitted optical power per volume in the interval $[\lambda_2, \lambda_1]$ | $\mathrm{W\,m^{-3}}$ |
> | $\lambda_1, \lambda_2$ | wavelength limits of the interval, $\lambda_1>\lambda_2$ | $\mathrm{m}$ |
> | $p_{\lambda}(\lambda_{\mathrm c})$ | spectral power density per wavelength at the center wavelength | $\mathrm{W\,m^{-4}}$ |
> | $\lambda_{\mathrm c}$ | center wavelength of the interval | $\mathrm{m}$ |
> | $\Delta\lambda$ | width of the wavelength interval (spectrometer bandwidth) | $\mathrm{m}$ |
