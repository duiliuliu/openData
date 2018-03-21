const tape = require('tape')
const n = require('./')

tape('electron-shortcut-normalizer', function (test) {
  eq = test.equal
  eq(typeof n, 'function', 'is a function')
  eq(n('Ctrl+B'), 'CommandOrControl+B', 'makes your keyboard shortcuts platform-agnostic')
  eq(n('CommandOrControl+X', 'darwin'), 'Command+X', 'can make them platform-specific too')
  eq(n('CommandOrControl+K', {platform: 'darwin'}), 'Command+K', 'accepts target `platform` in an options object')
  eq(n('CmdOrCtrl+Option+a', 'darwin'), 'Command+Alt+A', 'converts Option to Alt, because Alt exists on all platforms')
  eq(n('CmdOrCtrl+y', 'darwin'), 'Command+Y', 'converts `CmdOrCtrl` modifier to `CommandOrControl`')
  eq(n('Shift+VolumeUp+MediaPreviousTrack'), 'Shift+VolumeUp+MediaPreviousTrack', 'supports mixed-case modifiers like `MediaPreviousTrack`')
  eq(n('ctrl+w'), 'CommandOrControl+W', 'capitalizes first letter of each modifier')
  eq(n(' Ctrl + A '), 'CommandOrControl+A', 'removes whitespace from shorcuts')
  eq(n('ctrl-alt-o'), 'CommandOrControl+Alt+O', 'converts hyphens (-) to plusses (+)')

  eq(n('Command+L', 'win32'), 'Control+L', 'converts mac shortcuts to windows')
  eq(n('Ctrl+L', 'win32'), 'Control+L', 'converts shorthand windows to longhand')
  eq(n('CmdOrCtrl+m', 'win32'), 'Control+M', 'converts longhand agnostic to windows')
  eq(n('CommandOrControl+N', 'win32'), 'Control+N', 'converts shorthand agnostic to windows')
  test.end()
})
