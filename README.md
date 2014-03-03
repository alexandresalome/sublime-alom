SublimeText Package by Alexandre Salomé
=======================================

This packages provides a shortcut to insert the `namespace` definition in a PHP file. It has support for PSR-0 style namespaces and support for PSR-4 if [Composer](https://getcomposer.org/doc/04-schema.md#psr-4) is used.

Installation
------------

To install the plugin under Linux:

    cd ~/.config/sublime-text-2/Packages
    git clone https://github.com/alexandresalome/sublime-alom Alom

This package provides:

* ``php_namespace``: Insert PHP namespace


Shortcuts for commands
----------------------

You can add it to your shortcuts: go to *Preferences*, *Key Bindings (User)* and
add the following lines:

    [
        {
            "keys": ["ctrl+alt+n"], "command": "php_namespace"
        }
    ]
