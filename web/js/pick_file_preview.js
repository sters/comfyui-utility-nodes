// Preview support for PickFile (issue #28 follow-up).
//
// PickFile is deliberately file-type-agnostic (see nodes/util/pick_file.py), so
// it can't blanket-opt into ComfyUI's built-in `image_upload` combo behavior
// the way LoadImage does -- that would try to render every non-image pick
// (video, audio, text, ...) as a broken image. Instead this shows the same
// thumbnail LoadImage shows, but only when the picked filename actually looks
// like an image; anything else just clears the preview.
import { app } from "../../scripts/app.js";
import { api } from "../../scripts/api.js";

const NODE_TYPE = "UtilityNodesPickFile";
const IMAGE_EXTENSIONS = /\.(png|jpe?g|gif|webp|bmp|svg)$/i;

app.registerExtension({
    name: "UtilityNodes.PickFilePreview",
    async beforeRegisterNodeDef(nodeType, nodeData) {
        if (nodeData.name !== NODE_TYPE) return;

        const onNodeCreated = nodeType.prototype.onNodeCreated;
        nodeType.prototype.onNodeCreated = function () {
            const result = onNodeCreated?.apply(this, arguments);

            const fileWidget = this.widgets?.find((w) => w.name === "file");
            if (!fileWidget) return result;

            const showPreview = (filename) => {
                if (!filename || !IMAGE_EXTENSIONS.test(filename)) {
                    delete this.imgs;
                    app.graph.setDirtyCanvas(true, true);
                    return;
                }
                const img = new Image();
                img.onload = () => {
                    this.imgs = [img];
                    this.setSizeForImage?.();
                    app.graph.setDirtyCanvas(true, true);
                };
                // Input files picked here are always at the input-dir root, so subfolder is always empty.
                // The rand param is just cache-busting, in case a re-uploaded file reuses the same name.
                img.src = api.apiURL(
                    `/view?filename=${encodeURIComponent(filename)}&type=input&subfolder=&rand=${Math.random()}`,
                );
            };

            const origCallback = fileWidget.callback;
            fileWidget.callback = function (value, ...rest) {
                showPreview(value);
                return origCallback?.apply(this, [value, ...rest]);
            };

            showPreview(fileWidget.value);
            return result;
        };
    },
});
