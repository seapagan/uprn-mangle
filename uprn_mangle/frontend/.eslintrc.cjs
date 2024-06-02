module.exports = {
  root: true,
  env: { browser: true, es2020: true },
  extends: [
    "eslint:recommended",
    "plugin:react/recommended",
    "plugin:react/jsx-runtime",
    "plugin:react-hooks/recommended",
  ],
  ignorePatterns: ["dist", ".eslintrc.cjs"],
  parserOptions: { ecmaVersion: "latest", sourceType: "module" },
  settings: { react: { version: "18.2" } },
  plugins: ["react-refresh", "simple-import-sort", "import"],
  rules: {
    "react/jsx-no-target-blank": "off",
    "react-refresh/only-export-components": [
      "warn",
      { allowConstantExport: true },
    ],
    "import/no-duplicates": "error",
    "import/first": "error",
    "import/newline-after-import": [
      "error",
      {
        "count": 1,
      },
    ],
    "indent": [
      "error",
      2,
      {
        "SwitchCase": 1,
      },
    ],
    "linebreak-style": ["error", "unix"],
    "max-len": [
      "warn",
      80,
      2,
      {
        "ignoreComments": false,
        "ignoreStrings": false,
        "ignoreUrls": true,
      },
    ],
    "no-unused-vars": "warn",
    "quotes": ["error", "double"],
    "react/prop-types": [
      "error",
      {
        "skipUndeclared": true,
      },
    ],
    "semi": ["error", "always"],
    "padding-line-between-statements": [
      "error",
      { "blankLine": "always", "prev": "*", "next": "return" },
    ],
    "simple-import-sort/exports": "error",
    "simple-import-sort/imports": [
      "error",
      {
        "groups": [
          ["react-app-polyfill"],
          ["^react$", "^next"],
          ["^react-dom", "^react-router-dom"],
          ["^[a-z]"],
          // Packages starting with `@`
          ["^@"],
          // Packages starting with `~`
          ["^~"],
          // Side effect imports
          ["^\\u0000"],
          // internal Components
          ["^components/", "^services/", "^constants"],
          // Imports starting with `../`
          ["^\\.\\.(?!/?$)", "^\\.\\./?$"],
          // Imports starting with `./`
          ["^\\./(?=.*/)(?!/?$)", "^\\.(?!/?$)", "^\\./?$"],
          // Style imports
          ["^.+\\.s?css$"],
        ],
      },
    ],
  },
};
