const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");

async function renderIcon(Icon, color, sizePx = 256) {
  const svgMarkup = ReactDOMServer.renderToStaticMarkup(
    React.createElement(Icon, { color: `#${color}`, size: sizePx })
  );
  const buf = await sharp(Buffer.from(svgMarkup)).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

module.exports = { renderIcon };
