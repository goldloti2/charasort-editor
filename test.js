dataSetVersion = "2025-05-31"; // Change this when creating a new data set version. YYYY-MM-DD format.
dataSet[dataSetVersion] = {};

dataSet[dataSetVersion].options = [
  {
    name: "Filter by Type",
    key: "type",
    tooltip: "Check this to restrict to characters attack type.",
    sub: [
      { name: "Glacio",  key: "glacio" },
      { name: "Fusion",  key: "fusion" },
      { name: "Electro", key: "electro" },
      { name: "Aero",    key: "aero" },
      { name: "Spectro", key: "spectro" },
      { name: "Havoc",   key: "havoc" },
    ]
  },
  {
    name: "Exclude Rover",
    key: "rover",
    tooltip: "Check this to not sorting with Rover.",
    checked: true,
  },
];

dataSet[dataSetVersion].characterData = [
  {
    name: "Verina",
    img: "T_IconRoleHead256_3_UI.webp",
    opts: {
      type: ["spectro"],
      weapon: ["rectifier"],
      rarity: ["s5"],
      version: ["10"],
      gender: ["female"],
    }
  },
  {
    name: "Male Rover",
    img: "T_IconRoleHead256_4_UI.webp",
    opts: {
      type: ["spectro", "spectro", "aero", "glacio", "fusion", "electro"],
      weapon: ["sword"],
      rarity: ["s5"],
      version: ["10"],
      gender: ["female"],
      rover: true
    }
  },
];
