const Lang = imports.lang;
const Applet = imports.ui.applet;
const DBus = imports.dbus;
const GLib = imports.gi.GLib;
const Gtk = imports.gi.Gtk;
const Gettext = imports.gettext.domain('cinnamon-applets');
const _ = Gettext.gettext;

const NeteInterface = {
    name: "de.fqxp.nete.MainController",
    methods: [
        { name: "toggle", inSignature: "", outSignature: "" }
    ]
}

const NeteInterfaceProxy = DBus.makeProxyClass(NeteInterface);
let neteProxy = new NeteInterfaceProxy(DBus.session, 'de.fqxp.nete', '/');

function NeteApplet(orientation) {
    this._init(orientation);
}

NeteApplet.prototype = {
    __proto__: Applet.IconApplet.prototype,

    _init: function(metadata, orientation) {
        Applet.IconApplet.prototype._init.call(this, orientation);

        try {
            Gtk.IconTheme.get_default().append_search_path(metadata.path);
            this.set_applet_icon_symbolic_name("notepad");
            this.set_applet_tooltip(_("Toggle nete main window"));
        }
        catch (e) {
            global.logError(e);
        }
     },

    on_applet_clicked: function(event) {
      neteProxy.toggleRemote();
    }
};

function main(metadata, orientation) {
    let applet = new NeteApplet(metadata, orientation);
    return applet;
}
