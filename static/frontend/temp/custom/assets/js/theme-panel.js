let url = window.location.href;
function findStringInURL(searchString) {
  const currentURL = window.location.href;
  return currentURL.includes(searchString);
}

function get_basename() {
  // Remove trailing slash if it exists
  if (url.endsWith("/")) {
    url = url.slice(0, -1);
  }

  // Get the basename
  return url.substring(url.lastIndexOf("/") + 1);
}

function ath_wp_footer_hook() {
  const siteUrl = window.location.href;

  const awaikenThemes = {
    "elixir-html": {
      buy_link: "https://1.envato.market/ZQ79Ok",
      landing_page_link: "https://demo.awaikenthemes.com/landing/elixir-html/",
      demo_link: "https://demo.awaikenthemes.com/html-preview/elixir/",
      doc_link: "",
    },
    "quivox-html": {
      buy_link: "https://1.envato.market/rQP2jj",
      landing_page_link: "https://demo.awaikenthemes.com/html-preview/quivox/",
      demo_link: "https://demo.awaikenthemes.com/html-preview/quivox/html/",
      doc_link: "",
    },
    "aziland-html": {
      buy_link: "https://1.envato.market/5gdkM1",
      landing_page_link: "https://demo.awaikenthemes.com/html-preview/aziland/",
      demo_link: "https://demo.awaikenthemes.com/html-preview/aziland/html/",
      doc_link: "",
      wp_demo: "https://demo.awaikenthemes.com/landing/aziland/",
    },
    "theme-aziland": {
      buy_link: "https://1.envato.market/QyoXqA",
      landing_page_link: "https://demo.awaikenthemes.com/landing/aziland/",
      demo_link: "https://demo.awaikenthemes.com/theme-aziland/",
      doc_link: "https://docs.awaikenthemes.com/aziland/",
    },
    "zorvixa-html": {
      buy_link: "https://1.envato.market/q43rJN",
      landing_page_link: "https://demo.awaikenthemes.com/html-preview/zorvixa/",
      demo_link: "https://demo.awaikenthemes.com/html-preview/zorvixa/html/",
      doc_link: "",
    },
    "jivux-html": {
      buy_link: "https://1.envato.market/B0JVPW",
      landing_page_link: "https://demo.awaikenthemes.com/html-preview/jivux/",
      demo_link: "https://demo.awaikenthemes.com/html-preview/jivux/html/",
      doc_link: "",
    },
    "fwizz-html": {
      buy_link: "https://1.envato.market/Qyrjoo",
      landing_page_link: "https://demo.awaikenthemes.com/html-preview/fwizz/",
      demo_link: "https://demo.awaikenthemes.com/html-preview/fwizz/html/",
      doc_link: "",
    },
    glimy: {
      buy_link: "https://1.envato.market/3eWgYy",
      landing_page_link: "",
      demo_link: "https://demo.awaikenthemes.com/glimy/",
      doc_link: "https://docs.awaikenthemes.com/glimy/",
    },
    "glimy-html": {
      buy_link: "https://1.envato.market/B0o109",
      landing_page_link: "https://demo.awaikenthemes.com/html-preview/glimy/",
      demo_link: "https://demo.awaikenthemes.com/html-preview/glimy/html/",
      doc_link: "",
    },
    solor: {
      buy_link: "https://1.envato.market/6e6KxK",
      landing_page_link: "https://demo.awaikenthemes.com/landing/solor/",
      demo_link: "https://demo.awaikenthemes.com/solor/",
      doc_link: "https://docs.awaikenthemes.com/solor/",
    },
    "solor-html": {
      buy_link: "https://1.envato.market/JzyeqR",
      landing_page_link: "https://demo.awaikenthemes.com/html-preview/solor/",
      demo_link: "https://demo.awaikenthemes.com/html-preview/solor/html/",
      doc_link: "",
      wp_demo: "https://demo.awaikenthemes.com/solor/",
    },
    weebix: {
      buy_link: "https://1.envato.market/Wq7m1M",
      landing_page_link: "https://demo.awaikenthemes.com/landing/weebix/",
      demo_link: "https://demo.awaikenthemes.com/weebix/",
      doc_link: "https://docs.awaikenthemes.com/weebix/",
    },
    "weebix-html": {
      buy_link: "https://1.envato.market/DKxV3y", //add to cart link
      landing_page_link: "https://demo.awaikenthemes.com/landing/weebix-html/",
      demo_link: "https://demo.awaikenthemes.com/html-preview/weebix/",
      doc_link: "",
    },
    "theme-aerologix": {
      buy_link: "https://1.envato.market/3egDGB",
      landing_page_link: "https://demo.awaikenthemes.com/landing/aerologix/",
      demo_link: "https://demo.awaikenthemes.com/theme-aerologix/",
      doc_link: "https://docs.awaikenthemes.com/aerologix/",
    },
    "aerologix-html": {
      buy_link: "https://1.envato.market/k0YBeN",
      landing_page_link:
        "https://demo.awaikenthemes.com/landing/aerologix-html/",
      demo_link: "https://demo.awaikenthemes.com/html-preview/aerologix/",
      doc_link: "",
      wp_demo: "https://demo.awaikenthemes.com/landing/aerologix/",
    },
    "theme-medipro": {
      buy_link: "https://1.envato.market/vNYR7e",
      landing_page_link: "https://demo.awaikenthemes.com/landing/medipro/",
      demo_link: "https://demo.awaikenthemes.com/theme-medipro/",
      doc_link: "https://docs.awaikenthemes.com/medipro/",
    },
    "medipro-html": {
      buy_link: "https://1.envato.market/xkY4Wv",
      landing_page_link: "https://demo.awaikenthemes.com/landing/medipro-html/",
      demo_link: "https://demo.awaikenthemes.com/html-preview/medipro/",
      doc_link: "",
      wp_demo: "https://demo.awaikenthemes.com/landing/medipro/",
    },
    wexico: {
      buy_link: "https://1.envato.market/DK7X7j",
      landing_page_link: "https://demo.awaikenthemes.com/landing/wexico/",
      demo_link: "https://demo.awaikenthemes.com/wexico/",
      doc_link: "https://docs.awaikenthemes.com/wexico/",
    },
    "wexico-html": {
      buy_link: "https://1.envato.market/eKYV9z",
      landing_page_link: "https://demo.awaikenthemes.com/landing/wexico-html/",
      demo_link: "https://demo.awaikenthemes.com/html-preview/wexico/",
      doc_link: "",
      wp_demo: "https://demo.awaikenthemes.com/landing/wexico/",
    },
    soare: {
      buy_link: "https://1.envato.market/5g4Ez2",
      landing_page_link: "https://demo.awaikenthemes.com/landing/soare/",
      demo_link: "https://demo.awaikenthemes.com/soare/",
      doc_link: "https://docs.awaikenthemes.com/soare/",
    },
    "soare-html": {
      buy_link: "https://1.envato.market/B07Zrq",
      landing_page_link: "https://demo.awaikenthemes.com/landing/soare-html/",
      demo_link: "https://demo.awaikenthemes.com/html-preview/soare/",
      doc_link: "",
    },
    seore: {
      buy_link: "https://1.envato.market/PyXY76",
      landing_page_link: "https://demo.awaikenthemes.com/landing/seore/",
      demo_link: "https://demo.awaikenthemes.com/seore/",
      doc_link: "https://docs.awaikenthemes.com/seore/",
    },
    "seore-html": {
      buy_link: "https://1.envato.market/XYJEoa",
      landing_page_link: "https://demo.awaikenthemes.com/landing/seore-html/",
      demo_link: "https://demo.awaikenthemes.com/html-preview/seore/",
      doc_link: "",
      wp_demo: "https://demo.awaikenthemes.com/landing/seore/",
    },
    builtup: {
      buy_link: "https://1.envato.market/rQZGEj",
      landing_page_link: "https://demo.awaikenthemes.com/landing/builtup/",
      demo_link: "https://demo.awaikenthemes.com/builtup/",
      doc_link: "https://docs.awaikenthemes.com/builtup/",
    },
    "builtup-html": {
      buy_link: "https://1.envato.market/y2VaAy",
      landing_page_link: "https://demo.awaikenthemes.com/landing/builtup-html/",
      demo_link: "https://demo.awaikenthemes.com/html-preview/builtup/",
      doc_link: "",
      wp_demo: "https://demo.awaikenthemes.com/builtup/",
    },
    dentaire: {
      buy_link: "https://awaikenthemes.com/buy-dentaire/",
      landing_page_link: "https://demo.awaikenthemes.com/landing/dentaire/",
      demo_link: "https://demo.awaikenthemes.com/dentaire/",
      doc_link: "https://docs.awaikenthemes.com/dentaire/",
    },
    "dentaire-html": {
      buy_link: "https://1.envato.market/oq2RPY",
      landing_page_link:
        "https://demo.awaikenthemes.com/landing/dentaire-html/",
      demo_link: "https://demo.awaikenthemes.com/html-preview/dentaire/",
      doc_link: "",
      wp_demo: "https://demo.awaikenthemes.com/primecare/demo3/",
    },
    physiocare: {
      buy_link: "https://awaikenthemes.com/buy-physiocare/",
      landing_page_link: "https://demo.awaikenthemes.com/landing/physiocare/",
      demo_link: "https://demo.awaikenthemes.com/physiocare/",
      doc_link: "https://docs.awaikenthemes.com/physiocare/",
    },
    "physiocare-html": {
      buy_link: "https://1.envato.market/baZbv6",
      landing_page_link:
        "https://demo.awaikenthemes.com/landing/physiocare-html/",
      demo_link: "https://demo.awaikenthemes.com/html-preview/physiocare/",
      doc_link: "",
      wp_demo: "https://demo.awaikenthemes.com/physiocare/",
    },
    "novaride-html": {
      buy_link: "https://1.envato.market/21PkXG",
      landing_page_link:
        "https://demo.awaikenthemes.com/landing/novaride-html/",
      demo_link: "https://demo.awaikenthemes.com/html-preview/novaride/",
      doc_link: "",
      wp_demo: "https://demo.awaikenthemes.com/landing/novaride/",
    },
    novaride: {
      buy_link: "https://1.envato.market/nLr31o",
      landing_page_link: "https://demo.awaikenthemes.com/landing/novaride/",
      demo_link: "https://demo.awaikenthemes.com/novaride/",
      doc_link: "https://docs.awaikenthemes.com/novaride/",
    },
    "avenix-html": {
      buy_link: "https://1.envato.market/Y9Onke",
      landing_page_link: "https://demo.awaikenthemes.com/landing/avenix-html/",
      demo_link: "https://demo.awaikenthemes.com/html-preview/avenix/",
      doc_link: "",
      wp_demo: "https://demo.awaikenthemes.com/avenix/",
    },
    avenix: {
      buy_link: "https://1.envato.market/3e2ZMr",
      landing_page_link: "https://demo.awaikenthemes.com/landing/avenix/",
      demo_link: "https://demo.awaikenthemes.com/avenix/",
      doc_link: "https://docs.awaikenthemes.com/avenix/",
    },
    "florax-html": {
      buy_link: "https://1.envato.market/baLNgg",
      landing_page_link: "https://demo.awaikenthemes.com/landing/florax-html/",
      demo_link: "https://demo.awaikenthemes.com/html-preview/florax/",
      doc_link: "",
      wp_demo: "https://demo.awaikenthemes.com/florax/",
    },
    florax: {
      buy_link: "https://1.envato.market/9g4m3Y",
      landing_page_link: "https://demo.awaikenthemes.com/landing/florax/",
      demo_link: "https://demo.awaikenthemes.com/florax/",
      doc_link: "https://docs.awaikenthemes.com/florax/",
    },
    "primecare-html": {
      buy_link: "https://1.envato.market/ZQPQJk",
      landing_page_link:
        "https://demo.awaikenthemes.com/landing/primecare-html/",
      demo_link: "https://demo.awaikenthemes.com/html-preview/primecare",
      doc_link: "",
      wp_demo: "https://demo.awaikenthemes.com/primecare/",
    },
    primecare: {
      buy_link: "https://1.envato.market/6e2Kmb",
      landing_page_link: "https://demo.awaikenthemes.com/landing/primecare/",
      demo_link: "https://demo.awaikenthemes.com/primecare/",
      doc_link: "https://docs.awaikenthemes.com/primecare/",
    },
    carefirst: {
      buy_link: "https://awaikenthemes.com/buy-carefirst/",
      landing_page_link: "https://demo.awaikenthemes.com/landing/carefirst/",
      demo_link: "https://demo.awaikenthemes.com/carefirst/",
      doc_link: "https://docs.awaikenthemes.com/carefirst/",
    },
    "carefirst-html": {
      buy_link: "https://1.envato.market/VmzX1O",
      landing_page_link:
        "https://demo.awaikenthemes.com/landing/carefirst-html/",
      demo_link: "https://demo.awaikenthemes.com/html-preview/carefirst/",
      doc_link: "",
      wp_demo: "https://demo.awaikenthemes.com/carefirst/",
    },
    "leadz-html": {
      buy_link: "https://1.envato.market/6e29bN",
      landing_page_link: "https://demo.awaikenthemes.com/landing/leadz-html/",
      demo_link: "https://demo.awaikenthemes.com/html-preview/leadz/",
      doc_link: "",
      wp_demo: "https://demo.awaikenthemes.com/leadz/",
    },
    leadz: {
      buy_link: "https://1.envato.market/wp-leadz",
      landing_page_link: "https://demo.awaikenthemes.com/landing/leadz/",
      demo_link: "https://demo.awaikenthemes.com/leadz/",
      doc_link: "https://docs.awaikenthemes.com/leadz/",
    },
    healthify: {
      buy_link: "https://awaikenthemes.com/buy-healthify/",
      landing_page_link: "https://demo.awaikenthemes.com/landing/healthify/",
      demo_link: "https://demo.awaikenthemes.com/healthify/",
      doc_link: "https://docs.awaikenthemes.com/healthify/",
    },
    "healthify-html": {
      buy_link: "",
      landing_page_link:
        "https://demo.awaikenthemes.com/landing/healthify-html/",
      demo_link: "https://demo.awaikenthemes.com/html-preview/healthify/",
      doc_link: "",
      wp_demo: "https://demo.awaikenthemes.com/healthify/",
    },
    levis: {
      buy_link: "https://1.envato.market/wp-levis",
      landing_page_link: "https://demo.awaikenthemes.com/landing/levis/",
      demo_link: "https://demo.awaikenthemes.com/levis/",
      doc_link: "https://docs.awaikenthemes.com/levis/",
    },
    "diggy-html": {
      buy_link: "https://1.envato.market/html-diggy",
      landing_page_link: "https://demo.awaikenthemes.com/landing/diggy-html/",
      demo_link: "https://demo.awaikenthemes.com/html-preview/diggy/",
      doc_link: "",
      wp_demo: "https://demo.awaikenthemes.com/diggy/",
    },
    diggy: {
      buy_link: "https://1.envato.market/diggy-wp",
      landing_page_link: "https://demo.awaikenthemes.com/landing/diggy/",
      demo_link: "https://demo.awaikenthemes.com/diggy/",
      doc_link: "https://docs.awaikenthemes.com/diggy/",
    },
    "brixo-html": {
      buy_link: "https://1.envato.market/brixo-html",
      landing_page_link: "https://demo.awaikenthemes.com/landing/brixo-html/",
      demo_link: "https://demo.awaikenthemes.com/html-preview/brixo/",
      doc_link: "",
      wp_demo: "https://demo.awaikenthemes.com/landing/brixo/",
    },
    brixo: {
      buy_link: "https://1.envato.market/brixo-wp",
      landing_page_link: "https://demo.awaikenthemes.com/landing/brixo/",
      demo_link: "https://demo.awaikenthemes.com/brixo/",
      doc_link: "https://docs.awaikenthemes.com/brixo/",
    },
    "infine-html": {
      buy_link: "https://1.envato.market/infine-html",
      landing_page_link: "https://demo.awaikenthemes.com/landing/infine-html/",
      demo_link: "https://demo.awaikenthemes.com/html-preview/infine/",
      doc_link: "",
      wp_demo: "",
    },
    infine: {
      buy_link: "https://1.envato.market/infine-wp",
      landing_page_link: "https://demo.awaikenthemes.com/landing/infine/",
      demo_link: "https://demo.awaikenthemes.com/infine/",
      doc_link: "https://docs.awaikenthemes.com/infine/",
    },
    "artistic-html": {
      buy_link: "https://1.envato.market/artistic-html",
      landing_page_link:
        "https://demo.awaikenthemes.com/landing/artistic-html/",
      demo_link: "https://demo.awaikenthemes.com/html-preview/artistic/",
      doc_link: "",
      wp_demo: "https://demo.awaikenthemes.com/landing/artistic/",
    },
    artistics: {
      buy_link: "https://1.envato.market/artistic-wp",
      landing_page_link: "https://demo.awaikenthemes.com/landing/artistic/",
      demo_link: "https://demo.awaikenthemes.com/artistics/",
      doc_link: "https://docs.awaikenthemes.com/artistics/",
    },
    "awning-html": {
      buy_link: "https://1.envato.market/awning-html",
      landing_page_link: "https://demo.awaikenthemes.com/landing/awning-html/",
      demo_link: "https://demo.awaikenthemes.com/html-preview/awning/",
      doc_link: "",
      wp_demo: "",
    },
    "toplax-html": {
      buy_link: "https://1.envato.market/toplax-html",
      landing_page_link: "https://demo.awaikenthemes.com/landing/toplax/",
      demo_link: "https://demo.awaikenthemes.com/html-preview/toplax/",
      doc_link: "",
      wp_demo: "",
    },
    toplax: {
      buy_link: "https://1.envato.market/toplax-wp",
      landing_page_link: "https://demo.awaikenthemes.com/landing/toplax/",
      demo_link: "https://demo.awaikenthemes.com/toplax/",
      doc_link: "https://docs.awaikenthemes.com/toplax/",
    },
    "hipno-html": {
      buy_link: "https://1.envato.market/hipno-html",
      landing_page_link: "https://demo.awaikenthemes.com/landing/hipno/",
      demo_link: "https://demo.awaikenthemes.com/html-preview/hipno/",
      doc_link: "",
      wp_demo: "",
    },
    hipno: {
      buy_link: "https://1.envato.market/hipno-wp",
      landing_page_link: "https://demo.awaikenthemes.com/landing/hipno/",
      demo_link: "https://demo.awaikenthemes.com/hipno/",
      doc_link: "https://docs.awaikenthemes.com/hipno/",
    },
    netto: {
      buy_link: "https://1.envato.market/netto-wp",
      landing_page_link: "https://demo.awaikenthemes.com/landing/netto/",
      demo_link: "https://demo.awaikenthemes.com/netto/",
      doc_link: "https://docs.awaikenthemes.com/netto/",
    },
    "inspaire-html": {
      buy_link: "https://1.envato.market/inspairehtml",
      landing_page_link: "https://demo.awaikenthemes.com/landing/inspaire/",
      demo_link: "https://demo.awaikenthemes.com/html-preview/inspaire/",
      doc_link: "",
      wp_demo: "",
    },
    inspaire: {
      buy_link: "https://1.envato.market/inspaire-wp",
      landing_page_link: "https://demo.awaikenthemes.com/landing/inspaire/",
      demo_link: "https://demo.awaikenthemes.com/inspaire/",
      doc_link: "https://docs.awaikenthemes.com/inspaire/",
    },
  };

  let buy_link = "";
  let doc_link = "";
  let demo_link = "";
  let item = "";
  let wp_demo = "";

  if (findStringInURL("html-preview")) {
    var item_name = url.split("/html-preview/")[1]?.split("/")[0];
    item = item_name + "-html";
  } else {
    item = url.replace(window.location.origin + "/", "").split("/")[0];
  }

  if (awaikenThemes[item]) {
    buy_link = awaikenThemes[item]["buy_link"];

    if (awaikenThemes[item]["doc_link"]) {
      doc_link = awaikenThemes[item]["doc_link"];
    }

    if (awaikenThemes[item]["demo_link"]) {
      demo_link = awaikenThemes[item]["demo_link"];
    }

    if (awaikenThemes[item]["wp_demo"]) {
      wp_demo = awaikenThemes[item]["wp_demo"];
    }

    const themePanel = `
		<div class="explore_theme_panel">
			${
        doc_link
          ? `<a href="${doc_link}" target="_blank" title="Documentation"><i class="fas fa-file-lines"></i></a>`
          : ""
      }
			<a href="${buy_link}" target="_blank" title="Buy Now"><i class="fas fa-cart-shopping"></i></a> ${
      wp_demo
        ? `<a href="${wp_demo}" target="_blank" title="WordPress Theme Demo"><i class="fa-brands fa-wordpress"></i></a>`
        : ""
    }</div>
			<style type="text/css">
				.explore_theme_panel {
					width: 50px;
					position: fixed;
					top: 50%;
					right: 0;
					background: #fff;
					transform: translateY(-50%);
					border-top: 1px solid #e8e8e8;
					border-left: 1px solid #e8e8e8;
					border-bottom: 1px solid #e8e8e8;
					border-radius: 10px 0 0 10px;
					z-index: 10000;
				}
				.explore_theme_panel a {
					position: relative;
					width: 50px;
					height: 50px;
					display: flex;
					align-items: center;
					justify-content: center;
					font-size: 22px;
					color: #333;
					transition: all 0.4s ease-in-out;
					border-bottom: 1px solid #e8e8e8;
				}
				.explore_theme_panel a:last-child {
					border-bottom: none;
				}
				.demo-theme-popup {
  width: 390px;
  height: 120px;
  background: #FFF;
  bottom: 20px;
  right: -390px;
  position: fixed;
  border-radius: 5px;
  border:1px solid #0000001f;
  transition: 0.5s;
  z-index: 999;
  padding:35px 20px;
  color: #707070;
  font-size: 16px;
  text-align: center;
}
.demo-theme-popup a {
    font-weight: bold;
    color: #000;
    text-decoration: underline;
}

.dtp-close {
  position: absolute;
  top: 5px;
  right: 5px;
  width: 20px;
  height: 20px;
  cursor: pointer;
  z-index: 500;
}

.dtp-ns-close {
  width: 20px;
  height: 20px;
  position: absolute;
  right: 4px;
  top: 4px;
  overflow: hidden;
  text-indent: 100%;
  cursor: pointer;
  -webkit-backface-visibility: hidden;
  backface-visibility: hidden;
}
.dtp-ns-close:hover, .dtp-ns-close:focus {
  outline: none;
}
.dtp-ns-close::before, .dtp-ns-close::after {
  content: "";
  position: absolute;
  width: 3px;
  height: 60%;
  top: 50%;
  left: 50%;
  background: #fff;
}
.dtp-ns-close:hover::before, .dtp-ns-close:hover::after {
  background: #fff;
}
.dtp-ns-close::before {
  -webkit-transform: translate(-50%, -50%) rotate(45deg);
  transform: translate(-50%, -50%) rotate(45deg);
}
.dtp-ns-close::after {
  -webkit-transform: translate(-50%, -50%) rotate(-45deg);
  transform: translate(-50%, -50%) rotate(-45deg);
}

@keyframes dtp-bounce {
  0%, 20%, 50%, 80%, 100% {
    -moz-transform: translateY(0);
    -ms-transform: translateY(0);
    -webkit-transform: translateY(0);
    transform: translateY(0);
  }
  40% {
    -moz-transform: translateY(-30px);
    -ms-transform: translateY(-30px);
    -webkit-transform: translateY(-30px);
    transform: translateY(-30px);
  }
  60% {
    -moz-transform: translateY(-15px);
    -ms-transform: translateY(-15px);
    -webkit-transform: translateY(-15px);
    transform: translateY(-15px);
  }
}

.dtp-bounce {
  -moz-animation: bounce 2s infinite;
  -webkit-animation: bounce 2s infinite;
  animation: bounce 2s infinite;
}

@media (max-width: 728px) {
  .demo-theme-popup {
    width: 280px;
  }
}
			</style>`;
    document.body.insertAdjacentHTML("beforeend", themePanel);

    // Select all elements with the .buy-link class
    const buyLinkElements = document.querySelectorAll(".buy-link");

    // Loop through each element and set the href attribute
    buyLinkElements.forEach((element) => {
      element.href = buy_link;
    });

    // Select all elements with the .demo-link class
    const demoLinkElements = document.querySelectorAll(".demo-link");

    // Loop through each element and set the href attribute
    demoLinkElements.forEach((element) => {
      element.href = demo_link;
    });

    if (awaikenThemes[item]["wp_demo"]) {
      console.log(awaikenThemes[item]["wp_demo"]);

      /* Popup */

      var popup = document.createElement("div");
      popup.classList.add("demo-theme-popup");
      popup.innerHTML = `<div class="">
    <div class="dtp-close dtp-ns-close"></div>
	Looking For WordPress Theme? <br> <a href="${wp_demo}" target="_blank" title="WordPress Theme Demo">View Demo</a>
  </div>`;
      document.body.appendChild(popup);

      //document.addEventListener("DOMContentLoaded", function() {
      window.addEventListener("scroll", function () {
        const threshold = 1000;
        //if (window.scrollY >= (document.documentElement.scrollHeight - window.innerHeight - 4500)) {
        if (
          window.scrollY + window.innerHeight >=
          document.documentElement.scrollHeight - threshold
        ) {
          popup.style.right = "20px";
        } else {
          popup.style.right = "-390px";
        }
      });

      document
        .querySelector(".dtp-close")
        .addEventListener("click", function () {
          document.querySelector(".dtp-popup").style.display = "none";
        });
      //});

      /* Popup */
    }
  }
}

document.addEventListener("DOMContentLoaded", ath_wp_footer_hook);
