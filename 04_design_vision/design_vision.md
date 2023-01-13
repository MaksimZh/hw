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

Этот код проводит математические расчёты.
Помимо расчёта в программе присутствует логика чтения и сохранения результата.
Расчёты проводятся только для тех комбинаций параметров, которых в файле ещё нет.
Дополнительно, есть вывод на экран (фактически - логирование).

Итак, у нас три направления действий, которые на уровне логики связаны слабо,
а в коде перемешаны.
Чтобы их расцепить и причесать нужно лучше формализовать что
происходит на каждом направлении.


### Расчёт

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
    solve --> lr(localization_rate)

    classDef data fill:#afa, stroke:#000
    classDef proc fill:#faa, stroke:#000
    class mat,imp,ang,rh,en,eq,rad,lr data
    class crh,meq,solve proc
```

Параметры `material` (в коде - `x`) и `energy` меняются.
При этом для данного `material` нужно провести предварительные расчёты,
результаты которых будут общими для всех значений `energy`.

В этой части логики мы сосредоточимся на расчётах.
Поэтому считаем, что нам уже даны наборы материалов `material_collection`
и значений энергии `energy_collection`.
Остальные параметры задаются фиксированными и не меняются.

Для каждого материала решается задача при всех необходимых значениях энергии:
При этом наборы энергий для разных материалов могут отличаться,
потому что для каких-то материалов часть спектра уже может быть вычислена.
```mermaid
graph TD;
    mat(material) --> calc(calc_spectrum)
    en(energy_collection) --> calc
    calc --> lr(localization_rate_spectrum)

    classDef data fill:#afa, stroke:#000
    classDef proc fill:#faa, stroke:#000
    class mat,en,lr data
    class calc proc
```
Все остальные параметры спрятаны в `calc_spectrum`.


### Ввод и вывод


### Логирование
