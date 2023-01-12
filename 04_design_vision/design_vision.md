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

Этот код проводит математические расчёты и сохраняет результаты в файле.

Логика расчёта линейная:
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

Параметры `material` (в коде - `x`) и `energy` меняются.
При этом для данного `material` нужно провести предварительные расчёты,
которые будут общими для всех `energy`.

Помимо расчёта в программе присутствует логика чтения и сохранения результата.
Расчёты проводятся только для тех комбинаций параметров, которых в файле ещё нет.
Дополнительно, есть вывод на экран (фактически - логирование).

Итак, у нас три направления действий, которые на уровне логики связаны слабо,
а в коде перемешаны.
Чтобы их расцепить и причесать нужно лучше формализовать что
происходит на каждом направлении.

### Расчёт
### Ввод и вывод
### Логирование
