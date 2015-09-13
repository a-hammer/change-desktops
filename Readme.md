# Change All Desktops

Set a desktop picture on all desktops on OS X.

OS X 10.9+. Python 2.7.


## Usage

To set a picture for all desktops:

    python desktops.py picture

Without arguments, lists recent desktop pictures:

    python desktops.py


## Note

- For changes to take effect, the Dock is restarted. As a result, all minimized windows are maximized.
- The script modifies the desktop picture database `~/Library/Application Support/Dock/desktoppicture.db`. If you want to be catious, back up this file before running the script.


## See also

- [Gist by gregneagle](https://gist.github.com/gregneagle/6225747)
- [Overview](http://1klb.com/posts/2013/11/02/desktop-background-on-os-x-109-mavericks/) of the desktop pictures database
