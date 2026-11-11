import { app } from "../../scripts/app.js";

const MAX = 64;

app.registerExtension({
    name: "Prompter.nodes",
    async beforeRegisterNodeDef(nodeType, nodeData) {
        if (nodeData.name === "Prompter" || nodeData.name === "PrompterWomans") {
            // Show the chosen prompt in the text box after each run
            const onExecuted = nodeType.prototype.onExecuted;
            nodeType.prototype.onExecuted = function (message) {
                onExecuted?.apply(this, arguments);
                const w = this.widgets?.find((w) => w.name === "text");
                if (w && message?.text?.length) {
                    w.value = message.text[0];
                    this.setDirtyCanvas(true, true);
                }
            };
        }

        if (nodeData.name === "PrompterJoin") {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            nodeType.prototype.onNodeCreated = function () {
                onNodeCreated?.apply(this, arguments);
                // Start with 2 inputs; the rest are added with "+"
                for (let i = this.inputs.length - 1; i >= 2; i--) this.removeInput(i);

                this.addWidget("button", "✚ add prompt", null, () => {
                    if (this.inputs.length >= MAX) return;
                    this.addInput(`prompt_${this.inputs.length + 1}`, "STRING");
                    this.setSize(this.computeSize());
                });
                this.addWidget("button", "✖ remove last", null, () => {
                    if (this.inputs.length <= 1) return;
                    this.removeInput(this.inputs.length - 1);
                    this.setSize(this.computeSize());
                });
                this.setSize(this.computeSize());
            };
        }
    },
});
