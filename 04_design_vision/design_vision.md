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

Этот код вычисляет **спектры** (зависимость **степени локализации** от **энергии**)
для разных **материалов** (которые различаются параметром `x`).

**Набор энергий**, для которых нужны расчёты задаётся на входе.

Материал, **угловые параметры** (j, l), **параметры примеси** (z, z1, l1) и **температура** (t)
определяют **модель** для расчёта.

Результат записывается в **хранилище спектров**.

Если в хранилище уже есть спектр для данной модели,
то при необходимости он дополняется значениями для недостающих энергий.

Для каждого материала проводится предварительный расчёт **гамильтониана**,
общий для всех значений энергии.

Чтобы ждать результата было не скучно, на экран выводится данные о
**прогрессе** расчёта.

Слова выделенные жирным шрифтом - это компоненты логики программы.
Причём некоторые из них (например материал и гамильтониан) имеют большие перспективы
применения и в других моих расчётных программах.

Хорошо бы выделить их в коде явно.
