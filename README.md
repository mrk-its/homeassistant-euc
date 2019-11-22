# homeassistant-euc

Homeassistant custom component for Electric Unicycles integration

## Supported wheels

Integration works with wheels supported by python euc library - currently KingSong only, but other wheels should appear soon.

## Prerequisites

Working bluez bluetooth stack (over DBUS). You can verify if it works by manual installation of python libraries and running:
```
pip install euc.kingsong  # other backends supported by WheelLog should be available soon
python -m euc.cli
```
Above command should connect to nearby wheel and start displaying data.

## Instalation

Place directory **euc** in custom_components directory of your HASS installation (or create symlink **custom_components/euc** pointing to euc directory of cloned repository). In homeassistant go to Configuration / Integrations page and search for "Electric Unicycle" integration. After adding integration new sensors of basic wheel parameters should be visible.

Currently integration is read-only (only sensors are available), but rw access is also planned.
