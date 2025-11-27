# 100 Prisoners Simulator

A Python simulation of the **100 prisoners problem**, where each prisoner must find their own number hidden in one of 100 boxes.  
This project allows you to run multiple simulations using **custom strategies**, view success rates, and manage runs through a clean **simulation ID** system.

If you have any questions or suggestions, feel free to open an issue or submit a pull request! It would make my day. 😊

---

## 🎯 Features
- Run a predefined number of simulations automatically
- Use **custom strategies** for box selection
- Customize the number of prisoners and maximum box checks
- Calculate and display:
  - Overall chance of success
  - Average number of checked boxes per prisoner
  - Percentage of finds per prisoner
- Built-in simulation management using IDs for saving and loading configuration and progress

---

## 🧠 About the Project
I created this simulator because I wanted a way to **easily prove the math** behind the 100 prisoners problem, and to **experiment with different strategies** that people come up with, maybe even stumble upon a new, better one. 😉

The 100 prisoners problem is a classic probability and logic puzzle. Each prisoner may open up to half the boxes (50) to find their number.  
If **all** prisoners succeed, they are freed; if even one fails, they all lose.

---

## 📺 Video explanation & best strategy

A clear video explanation of the 100 prisoners problem and the best strategy so far (cycle following) can be found here:
https://youtu.be/iSNsgj1OCLA?si=Bgq4OAlChz_tSI_g

---

## ⚙️ Usage
1. Download the [latest release](https://github.com/TechRedByte/Prisoners-Riddle/releases/latest)
2. Unzip the downloaded .zip file
3. Customize the simulation settings and the strategy in config.py
4. Run the main Python file:
   ```bash
   python main.py
   ```
---

## 📜 License

MIT License - feel free to contribute or share it.

See LICENSE.md for details.

---

## 🧩 Future Ideas
- Better GUI
- Parallelized simulations for faster results
