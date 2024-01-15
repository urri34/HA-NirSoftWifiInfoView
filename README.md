# HA-NirSoftWifiInfoView
Contains the python script I use to view which is the best channel to put my zigbee on.

## NirSoftWifiInfoView.py:
### Issues:
- Living in a medium/high human density environment leads us to a medium/high wifi AP density.
- When implementing a Zigbee network for our home, we must choose a channel that it's not noisy.
- I want to see it in a graphical way.

### Solution:
- Use Nirsfot wifi info software to capture the signals aroud you.
- Process it using NirSoftWifiInfoView.py
- Enjoy taking the right channel choice decision.

### Nirsoft:
Download the software from:

https://www.nirsoft.net/utils/wifi_information_view.html

Execute it and keep it capturing wifi traffic for a while.
Now we are going to save all the captured data, got to "File" -> "Save All Items" -> "Save as type" -> "Comma Delimited text File (*.csv)" -> WriteDownSomeNiceName.csv

### Python:

Create some venv, don't we dirty and keep your computer clean, not like your room ... I can smell it even from github.
```sh
python -m venv venv
.\venv\Scripts\Activate.ps1 {If running on PowerShell}
venv\Scripts\activate.bat {If running on cmd}
./venv/Scripts/activate {If running on linux}
```

Install the requirements for this script:

```sh
pip install -r requirements.txt
```
Obtained from:


VmUUID part:
>C:\Program Files\Oracle\VirtualBox\VBoxManage.exe list --long vms
>
>Name:                        TestHA
>
>Encryption:     disabled
>
>Groups:                      /
>
>Guest OS:                    Linux (64-bit)
>
>UUID:                        `f05c746c-a545-4329-8252-bc3b42907131`
>
>Config file:                 C:\TestHA.vbox
>
>Snapshot folder:             C:\Snapshots
>
>Log folder:                  C:\Logs
>
>Hardware UUID:               `f05c746c-a545-4329-8252-bc3b42907131`

USBUUIDS part:
>UUID:               `6f06b710-ee69-4e5d-917b-d0808827102c`
>
> VendorId:           0x138a (138A)
>
> ProductId:          0x00ab (00AB)
>
> Revision:           1.100 (01100)
>
> Port:               8
>
> USB version/speed:  2/Full
>
> Manufacturer:       Wifi USB Stick Realteck
>
> Address:            {53d29ef7-377c-4d14-864b-eb3a85769359}\0000
>
> Current State:      Busy

(...)
>UUID:               `93cedeaf-a6f8-49c2-ab9e-0192aa434ba2`
>
> VendorId:           0x0bda (0BDA)
>
> ProductId:          0x8153 (8153)
>
> Revision:           49.0 (4900)
>
> Port:               2
>
> USB version/speed:  3/Super
>
> Manufacturer:       Realtek Semiconductor Corp.
>
> Product:            RTL8153 Zigbee Adapter
>
> Address:            {4d36e972-e325-11ce-bfc1-08002be10318}\0020
>
> Current State:      Busy

## Extra bonus
### Hide shutdown/reboot button
My windows10 machine where I run my OracleVM with my VM inside is connected to the TV so the kids can play Netflix and wotch only stuff thru the browsers. But My wife sometimes forget that the HAServer is running in background and just shutdown the server after whatching a film. Avoid it!
>
>HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\PolicyManager\default\Start\HideShutDown
>
