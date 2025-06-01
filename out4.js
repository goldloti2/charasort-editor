dataSetVersion = "2025-05-31";
dataSet[dataSetVersion] = {};
dataSet[dataSetVersion].options = [{
    name: "Exclude Rover",
    key: "rover",
    tooltip: "Check this to not sorting with Rover.",
    checked: true
}, {
    name: "Filter by Type",
    key: "TEST",
    tooltip: "Check this to restrict to characters attack type.",
    checked: false,
    sub: [{
        name: "Glacio",
        key: "glacio"
    }, {
        name: "Fusion",
        key: "fusion"
    }, {
        name: "Electro",
        key: "electro"
    }, {
        name: "Aero",
        key: "aero"
    }, {
        name: "Spectro",
        key: "spectro"
    }, {
        name: "Havoc",
        key: "havoc"
    }, AAA]
}];
dataSet[dataSetVersion].characterData = [{
    name: "Verina",
    img: "T_IconRoleHead256_3_UI.webp",
    opts: {
        type: ["spectro"],
        weapon: ["rectifier"],
        rarity: ["s5"],
        version: ["10"],
        gender: ["female"]
    }
}, {
    name: "Male Rover",
    img: "T_IconRoleHead256_4_UI.webp",
    opts: {
        type: ["spectro", "spectro", "aero"],
        weapon: ["sword"],
        rarity: ["s5"],
        version: ["10"],
        gender: ["female"],
        rover: true
    }
}];

