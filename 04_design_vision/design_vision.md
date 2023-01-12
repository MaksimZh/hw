# Увидеть ясную структуру дизайна
Если абстрагироваться от нескольких вложенных циклов, вывода прогресса на экран и записи результата в файл,
то программа просто выполняет расчёты для занного набора параметров и сохраняет результат:
```mermaid
graph TD;
    imp(ImpurityParams) --> calc(calculate)
    ang(AngularParams) --> calc
    mat(MaterialCollection) --> calc
    en(EnergyCollection) --> calc
    rad(RadiusMesh) --> calc
    calc --> wf(AllWavefunctionCollection)
    calc --> lr(AllLocalizationRateCollection)

    classDef proc fill:#faa, stroke:#000
    classDef data fill:#afa, stroke:#000
    class imp,ang,mat,en,rad,wf,lr data
    class calc proc
```


```mermaid
graph TD;
    ham(HamiltonianParams) --> calc(calculate)
    ang(AngularParams) --> calc
    en(EnergyCollection) --> calc
    rad(RadiusMesh) --> calc
    calc --> wf(WavefunctionCollection)
    calc --> lr(LocalizationRateCollection)

    classDef proc fill:#faa, stroke:#000
    classDef data fill:#afa, stroke:#000
    class ham,ang,en,rad,wf,lr data
    class calc proc
```

```mermaid
graph TD;
    hp(HamiltonianParams) --> calc_h(calc_hamiltonian)
    calc_h --> ham(Hamiltonian)
    ham --> calc_sh(calc_spherical_hamiltonian)
    ang(AngularParams) --> calc_sh
    calc_sh --> sh(SphericalHamiltonian)
    sh --> calc_eq(calc_equation_params)
    en(Energy) --> calc_eq
    calc_eq --> eq(RadialEquationParams)
    eq --> solve(solve_equation)
    rad(RadiusMesh) --> solve
    solve --> wf(Wavefunction)
    solve --> lr(LocalizationRate)

    classDef proc fill:#faa, stroke:#000
    classDef data fill:#afa, stroke:#000
    class hp,ang,ham,sh,en,eq,rad,wf,lr data
    class calc_h,calc_sh,calc_eq,solve proc
```
