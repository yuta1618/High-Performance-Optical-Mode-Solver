from lumina_fdfd import Simulation, Material

# 1. 屈折率の設定
Si = Material(3.48)
SiO2 = Material(1.44)
Air = Material(1.0)

# 2. シミュレーション領域の定義 (5um x 3um, 分解能 20nm)
sim = Simulation(window_size=(5.0, 3.0), resolution=(0.02, 0.02))

# 3. 構造の構築（下から順番に配置）
sim.add_rect(0, -0.5, 5.0, 2.0, SiO2)  # 基板 (Substrate)
sim.add_rect(0, 0.06, 5.0, 0.12, Si)   # スラブ層 (Slab)
sim.add_rect(0, 0.17, 0.5, 0.10, Si)   # リブ（コア部分）
sim.add_rect(0, 1.0, 5.0, 1.5, Air)    # クラッド (Cladding)

# 4. 固有モード解析 (波長 1.55um)
modes = sim.solve(wavelength=1.55, n_modes=1)

# 5. 可視化
modes[0].plot()