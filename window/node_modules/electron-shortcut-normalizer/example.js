const normalize = require('./')

// Make a shortcut platform-agnostic:
normalize('Ctrl+A')
// => 'CommandOrControl+A'

// Make a shortcut platform-specific:
normalize('CommandOrControl+Z', process.platform)
// => 'Command+Z' on Mac OS X
// => 'Control+Z' on Windows and Linux

// `Option` is unique to Mac OS X, so it's normalized to `Alt`:
normalize('CmdOrCtrl+Option+a', process)
// => 'Command+Alt+Z' on Mac OS X
// => 'Control+Alt+A' on Windows and Linux
