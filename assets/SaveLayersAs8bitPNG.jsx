// #target photoshop

(function () {
    var doc = app.activeDocument;
    var exportFolder = Folder.selectDialog("PNGを保存するフォルダを選択してください");

    if (!exportFolder) return; // キャンセル時

    var layers = getAllLayers(doc);

    if (layers.length === 0) {
        alert("書き出せるレイヤーがありません！");
        return;
    }

    var originalVisibility = {}; // 元の可視状態を保存

    // すべてのレイヤーの可視状態を保存して非表示にする
    for (var i = 0; i < layers.length; i++) {
        originalVisibility[layers[i].id] = layers[i].visible;
        layers[i].visible = false;
    }

    // 1レイヤーずつ表示して書き出し
    for (var i = 0; i < layers.length; i++) {
        var layer = layers[i];

        if (!originalVisibility[layer.id]) continue; // 元々非表示だったレイヤーはスキップ

        layer.visible = true; // 書き出すレイヤーを表示

        // レイヤーが属するフォルダ名（グループ名）を取得
        var groupName = getLayerGroupName(layer);
        if (!groupName) groupName = "Root"; // ルート直下なら "Root"

        // PNG保存
        var fileName = groupName + "_" + layer.name + ".png";
        var filePath = new File(exportFolder + "/" + fileName);
        saveAs8bitPNG(filePath);

        layer.visible = false; // 書き出し後に非表示に戻す
    }

    // 元の可視状態を復元
    for (var i = 0; i < layers.length; i++) {
        layers[i].visible = originalVisibility[layers[i].id];
    }

    alert("8bit PNG の書き出し完了！");

    function saveAs8bitPNG(file) {
        var pngOptions = new ExportOptionsSaveForWeb();
        pngOptions.format = SaveDocumentType.PNG;
        pngOptions.PNG8 = true; // 8bit PNG にする
        pngOptions.transparency = true;
        pngOptions.interlaced = false;
        pngOptions.quality = 100; // 品質最大

        doc.exportDocument(file, ExportType.SAVEFORWEB, pngOptions);
    }

    function getAllLayers(parent) {
        var layers = [];
        for (var i = 0; i < parent.layers.length; i++) {
            var layer = parent.layers[i];
            if (layer.typename === "LayerSet") {
                layers = layers.concat(getAllLayers(layer)); // グループの場合は再帰処理
            } else {
                layers.push(layer);
            }
        }
        return layers;
    }

    function getLayerGroupName(layer) {
        var parent = layer.parent;
        while (parent && parent.typename !== "Document") {
            if (parent.typename === "LayerSet") return parent.name; // 親がグループならその名前を返す
            parent = parent.parent;
        }
        return null; // グループに属していない場合
    }
})();
