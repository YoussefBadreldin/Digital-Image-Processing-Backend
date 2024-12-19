const express = require("express");
const multer = require("multer");
const { spawn } = require("child_process");
const path = require("path");

const app = express();
const upload = multer({ dest: "uploads/" });

app.use(express.static(path.join(__dirname, "../frontend/public")));

// Process Image
app.post("/process", upload.single("image"), (req, res) => {
    const action = req.body.action;
    const inputPath = req.file.path;
    const outputPath = `processed/processed_${req.file.filename}.png`;

    // Map actions to Python scripts
    const scriptMapping = {
        enhancement: "scripts/enhancement.py",
        compression: "scripts/compression.py",
        segmentation: "scripts/segmentation.py",
    };

    if (!scriptMapping[action]) {
        return res.status(400).send("Invalid action.");
    }

    // Run the corresponding Python script
    const pythonProcess = spawn("python", [
        scriptMapping[action],
        inputPath,
        outputPath,
    ]);

    pythonProcess.on("close", (code) => {
        if (code === 0) {
            res.json({ processedImage: outputPath });
        } else {
            res.status(500).send("Error processing image.");
        }
    });
});

// Serve Processed Images
app.get("/processed/:filename", (req, res) => {
    res.sendFile(path.join(__dirname, "processed", req.params.filename));
});

// Start Server
const PORT = 5000;
app.listen(PORT, () => console.log(`Backend running on http://localhost:${PORT}`));
