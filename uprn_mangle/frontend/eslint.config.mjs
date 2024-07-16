import _import from "eslint-plugin-import";
import reactRefresh from "eslint-plugin-react-refresh";
import simpleImportSort from "eslint-plugin-simple-import-sort";
import globals from "globals";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { fixupConfigRules, fixupPluginRules } from "@eslint/compat";
import { FlatCompat } from "@eslint/eslintrc";
import js from "@eslint/js";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const compat = new FlatCompat({
  baseDirectory: __dirname,
  recommendedConfig: js.configs.recommended,
  allConfig: js.configs.all
});

export default [{
  ignores: ["**/dist", "**/.eslintrc.cjs"],
}, ...fixupConfigRules(compat.extends(
  "eslint:recommended",
  "plugin:react/recommended",
  "plugin:react/jsx-runtime",
  "plugin:react-hooks/recommended",
)), {
  plugins: {
    "react-refresh": reactRefresh,
    "simple-import-sort": simpleImportSort,
    import: fixupPluginRules(_import),
  },

  languageOptions: {
    globals: {
      ...globals.browser,
    },

    ecmaVersion: "latest",
    sourceType: "module",
  },

  settings: {
    react: {
      version: "18.2",
    },
  },

  rules: {
    "react/jsx-no-target-blank": "off",

    "react-refresh/only-export-components": ["warn", {
      allowConstantExport: true,
    }],

    "import/no-duplicates": "error",
    "import/first": "error",

    "import/newline-after-import": ["error", {
      count: 1,
    }],

    indent: ["error", 2, {
      SwitchCase: 1,
    }],

    "linebreak-style": ["error", "unix"],

    "max-len": ["warn", 80, 2, {
      ignoreComments: false,
      ignoreStrings: false,
      ignoreUrls: true,
    }],

    "no-unused-vars": "warn",
    quotes: ["error", "double"],

    "react/prop-types": ["error", {
      skipUndeclared: true,
    }],

    semi: ["error", "always"],

    "padding-line-between-statements": ["error", {
      blankLine: "always",
      prev: "*",
      next: "return",
    }],

    "simple-import-sort/exports": "error",

    "simple-import-sort/imports": ["error", {
      groups: [
        ["react-app-polyfill"],
        ["^react$", "^next"],
        ["^react-dom", "^react-router-dom"],
        ["^[a-z]"],
        ["^@"],
        ["^~"],
        ["^\\u0000"],
        ["^components/", "^services/", "^constants"],
        ["^\\.\\.(?!/?$)", "^\\.\\./?$"],
        ["^\\./(?=.*/)(?!/?$)", "^\\.(?!/?$)", "^\\./?$"],
        ["^.+\\.s?css$"],
      ],
    }],
  },
}];