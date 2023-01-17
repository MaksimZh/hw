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

Этот код выполняет математические расчёты по следующей схеме:
```mermaid
graph TD
    x(x) --> clr(calc_localization_rate)
    t(temperature) --> clr
    mat --> clr
    ang(angular_params) --> clr
    imp(impurity_params) --> clr
    en(energy) --> clr
    rad(radial_mesh) --> clr
    clr --> lr(localization_rate)

    classDef data fill:#afa, stroke:#000
    classDef proc fill:#faa, stroke:#000
    class x,t,mat,imp,ang,en,rad,lr data
    class clr proc
```
Более подробно:
```mermaid
---
title: calc_localization_rate
---
graph TD
    x(x) --> ch(calc_hamiltonian)
    t(temperature) --> ch
    mat --> ch
    ang(angular_params) --> ch
    imp(impurity_params) --> ch
    ch --> h(hamiltonian)
    h --> solve(solve_schrodinger_equation)
    en(energy) --> solve
    rad(radial_mesh) --> solve
    solve --> lr(localization_rate)

    classDef data fill:#afa, stroke:#000
    classDef proc fill:#faa, stroke:#000
    class x,t,mat,imp,ang,h,en,rad,lr data
    class ch,solve proc
```
Следующий уровень:
```mermaid
---
title: calc_hamiltonian
---
graph TD
    x(x) --> mm(make_material)
    t(temperature) --> mm
    mm --> mat(material) 
    mat --> cbrh(calc_bulk_radial_hamiltonian)
    ang(angular_params) --> cbrh
    cbrh --> brh(bulk_radial_hamiltonian)
    brh --> crh(calc_radial_hamiltonian)
    imp(impurity_params) --> crh
    crh --> h(hamiltonian)

    classDef data fill:#afa, stroke:#000
    classDef proc fill:#faa, stroke:#000
    class x,t,mat,imp,ang,brh,h data
    class mm,cbrh,crh proc
```
```mermaid
---
title: solve_schrodinger_equation
---
graph TD
    h(hamiltonian) --> meq(make_equation)
    en(energy) --> meq
    meq --> eq(radial_equation)
    eq --> solve(solve)
    rad(radial_mesh) --> solve
    solve --> lr(localization_rate)

    classDef data fill:#afa, stroke:#000
    classDef proc fill:#faa, stroke:#000
    class h,en,eq,rad,wf,lr data
    class mm,cbrh,crh,meq,solve proc
```
При этом в данной программе меняются параметры `x` и `energy`,
но в других программах меняются другие параметры.