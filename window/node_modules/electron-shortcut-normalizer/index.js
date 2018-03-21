module.exports = function (shortcut, options) {

  if (!options) options = {}
  if (typeof options === 'string') options = {platform: options}

  shortcut = shortcut
    .replace(/\s/g, '')
    .replace(/-/g, '+')
    .replace(/option/i, 'Alt')
    .replace(/(commandorcontrol|cmdorctrl|ctrl|command)/i, 'CommandOrControl')
    .split('+')
    .map(part => part[0].toUpperCase() + part.slice(1))
    .join('+')

  switch (options.platform) {
    case 'darwin':
      return shortcut.replace('CommandOrControl', 'Command')
    case 'linux':
    case 'freebsd':
    case 'sunos':
    case 'win32':
      return shortcut.replace('CommandOrControl', 'Control')
    default:
      return shortcut
  }
}
