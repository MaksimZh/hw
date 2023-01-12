# Увидеть ясную структуру дизайна

## Что-то про квантовую механику - верхний уровень
```Python
...

def calc(params, energies, meshParams):
    r = solver.create_radial_mesh(meshParams)
    model = Hamiltonian(params)
    detQ = []
    for energy in energies:
        print(f"energy = {energy:6.2f}")
        detQ.append(np.linalg.det(solver.calc_localization_matrix(model, energy, meshParams)))
    detQ = np.array(detQ)
    return r, detQ, model.eg

for x in np.linspace(0, X_MAX, int(X_MAX / X_STEP + 0.1) + 1):
    params = SimpleNamespace(
        x = x,
        z = -1,
        j = args.j,
        l = args.l,
        t = 0,
        z1 = args.z1,
        l1 = args.l1,
    )
    with h5py.File(source_dir + fileName, "a") as f:
        key = paramKey(params)
        if key in f:
            print("exists", key)
            # calculation will be made only for missing energy values
            g = f[key]
            oldEnergies = g["energies"]
            calcEnergies = energies_meV[np.logical_not(
                np.isclose(energies_meV[:, np.newaxis], oldEnergies).any(1))]
            r, detQ, eg = calc(params, calcEnergies, meshParams)
            newEnergies = np.concatenate((oldEnergies, calcEnergies))
            s = np.argsort(newEnergies)
            newEnergies = newEnergies[s]
            newDetQ = np.concatenate((g["detQ"], detQ))[s]
            del g["energies"]
            del g["detQ"]
            g.create_dataset("energies", data=newEnergies)
            g.create_dataset("detQ", data=newDetQ)
            print()
        else:
            print("calculating", key)
            r, detQ, eg = calc(params, energies_meV, meshParams)
            print("creating", key)
            g = f.create_group(key)
            g.attrs["x"] = params.x
            g.attrs["z"] = params.z
            g.attrs["z1"] = params.z1
            g.attrs["l1"] = params.l1
            g.attrs["j"] = params.j
            g.attrs["l"] = params.l
            g.attrs["eg"] = eg
            g.create_dataset("energies", data=energies_meV)
            g.create_dataset("detQ", data=detQ)
            print()

...
```

Если абстрагироваться от нескольких вложенных циклов, вывода прогресса на экран и записи результата в файл,
то программа просто выполняет расчёты для заданного набора параметров и сохраняет результат:
```mermaid
graph TD;
    imp(impurity_params) --> calc(calculate)
    ang(angular_params) --> calc
    mat(material_collection) --> calc
    en(energy_collection) --> calc
    rad(radius_mesh) --> calc
    calc --> wf(wavefunction_spectrum_collection)
    calc --> lr(localization_rate_spectrum_collection)

    classDef proc fill:#faa, stroke:#000
    classDef data fill:#afa, stroke:#000
    class imp,ang,mat,en,rad,wf,lr data
    class calc proc
```
Если бы нам нужен был только один материал и одна энергия, то логика расчёта выглядела бы так:
```mermaid
graph TD;
    mat(material) --> crh(calc_radial_hamiltonian)
    imp(impurity_params) --> crh
    ang(angular_params) --> crh
    crh --> rh(radial_hamiltonian)
    rh --> meq(make_equation)
    en(energy) --> meq
    meq --> eq(radial_equation)
    eq --> solve(solve)
    rad(radius_mesh) --> solve
    solve --> wf(wavefunction)
    solve --> lr(localization_rate)

    classDef data fill:#afa, stroke:#000
    classDef proc fill:#faa, stroke:#000
    class mat,imp,ang,rh,en,eq,rad,wf,lr data
    class crh,meq,solve proc
```
Её нужно отделить от работы с коллекциями параметров.

Вычисление энергетического спектра для фиксированного материала -
это отдельная физическая задача.
Вот пусть логика это и отражает:
```mermaid
graph TD;
    imp(impurity_params) --> make(make_solver)
    ang(angular_params) --> make
    en(energy_collection) --> make
    rad(radius_mesh) --> make
    mat(material_collection) --> calc(calculate)
    subgraph calculate
        make --> solver(solve_for_material)
        solver --> calc
    end
    calc --> wf(wavefunction_spectrum_collection)
    calc --> lr(localization_rate_spectrum_collection)

    classDef data fill:#afa, stroke:#000
    classDef proc fill:#faa, stroke:#000
    class imp,ang,en,rad,mat,solver,wf,lr data
    class make,calc proc
```
где `solve_for_material` - это процедура решения задачи для одного материала:
```mermaid
graph TD;
    mat(material) --> solve(solve_for_material)
    solve --> wf(wavefunction_spectrum)
    solve --> lr(localization_rateSpectrum)

    classDef data fill:#afa, stroke:#000
    classDef proc fill:#faa, stroke:#000
    class mat,wf,lr data
    class solve proc
```
Внутри этой процедуры мы снова отделяем логику расчёта от работы с коллекциями:
```mermaid
graph TD;
    mat(material) --> make(make_energy_solver)
    subgraph solve_for_material
        ch(calc_hamiltonian_for_material) --> make
        se(solve_equation) --> make
        make --> solver(solve_for_energy)
        en(energy_collection) --> calc(calculate_for_material)
        solver --> calc
    end
    calc --> wf(wavefunction_spectrum)
    calc --> lr(localization_rateSpectrum)

    classDef data fill:#afa, stroke:#000
    classDef proc fill:#faa, stroke:#000
    class mat,ch,se,en,solver,wf,lr data
    class make,calc proc
```
Процедуры `calc_hamiltonian_for_material` и `solve_equation` - это замыкания:
```mermaid
graph TD;
    mat(material) --> crh(calc_radial_hamiltonian)
    subgraph calc_hamiltonian_for_material
        imp(impurity_params) --> crh
        ang(angular_params) --> crh
    end
    crh --> rh(radial_hamiltonian)
    rh --> meq(make_equation)
    en(energy) --> meq
    subgraph solve_equation
        meq --> eq(radial_equation)
        eq --> solve(solve)
        rad(radius_mesh) --> solve
    end
    solve --> wf(wavefunction)
    solve --> lr(localization_rate)

    classDef data fill:#afa, stroke:#000
    classDef proc fill:#faa, stroke:#000
    class mat,imp,ang,rh,en,eq,rad,wf,lr data
    class crh,meq,solve proc
```
Процедура `make_energy_solver` собирает их вместе:
```mermaid
graph TD;
    en(energy) --> solve
    subgraph solve_for_energy
        mat(material) --> crh(calc_hamiltonian_for_material)
        crh --> rh(radial_hamiltonian)
        rh --> solve(solve_equation)
    end
    solve --> wf(wavefunction)
    solve --> lr(localization_rate)

    classDef data fill:#afa, stroke:#000
    classDef proc fill:#faa, stroke:#000
    class mat,rh,en,wf,lr data
    class crh,meq,solve proc
```
Поскольку замыкание `solve_for_energy` помнит `radial_hamiltonian`,
он не вычисляется повторно для каждой энергии.

Кстати, у разных материалов могут быть разные `energy_collection`,
потому что какие-то энергии уже могли быть записаны в файл.

Процедуры `calculate` и `calculate_for_material` просто применяют решатели
к элементам соответствующих коллекций и упаковывают результаты в новые коллекции.
У них одинаковая логика и её тоже можно выделить.