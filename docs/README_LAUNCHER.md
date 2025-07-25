[![Build](https://img.shields.io/badge/build-passing-brightgreen)](https://github.com/tokintel/tokintel-v2/actions)
[![Test](https://img.shields.io/badge/tests-passing-brightgreen)](https://github.com/tokintel/tokintel-v2/actions)
[![Version](https://img.shields.io/badge/version-2.0.0-blue)](https://pypi.org/project/tokintel/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# TokIntel v2 – Launcher

## [INFO] Avvio rapido

### Windows

- Doppio click su `launch_tokintel.bat`
- **Oppure** da terminale:
  ```sh
  python streamlit_launcher.py
  ```

### Linux/Mac

- Da terminale:
  ```sh
  bash launch_tokintel.sh
  ```
  oppure
  ```sh
  python3 streamlit_launcher.py
  ```

---

## [INFO] Troubleshooting

- **UnicodeEncodeError**
  > Imposta la console su UTF-8:
  >
  > ```sh
  > chcp 65001
  > ```
- **streamlit: command not found**
  > Usa:
  >
  > ```sh
  > python -m streamlit run ...
  > ```

---

## [INFO] File launcher

- `launch_tokintel.bat`: Avvio rapido per Windows
- `launch_tokintel.sh`: Avvio rapido per Linux/Mac
- `streamlit_launcher.py`: Script universale per lanciare la UI

---

## 🏷️ Badge

- [OK] Tested
- 🌍 Cross-platform
- [REPORT] UI Ready 