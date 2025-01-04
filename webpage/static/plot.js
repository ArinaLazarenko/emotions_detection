const canvas = document.getElementById('plot');
const ctx = canvas.getContext('2d');
const tooltip = document.getElementById('tooltip');
const points = [];
const gridSize = 900; // Canvas width/height excluding margins
const margin = 50; // Space for labels
const axisMin = -20;
const axisMax = 20;
const unit = gridSize / (axisMax - axisMin); // Pixels per unit

const _label_to_color = {
    'anger': 'black',
    'fear': 'purple',
    'sadness': 'blue',
    'surprise': 'green',
    'joy': 'orange',
    'love': 'red'
};

function drawPlot() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Draw border
    ctx.strokeStyle = '#000';
    ctx.lineWidth = 1;
    ctx.strokeRect(margin, margin, gridSize, gridSize);

    // Draw labels outside the plot
    ctx.fillStyle = '#000';
    ctx.font = '12px Arial';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';

    // X-axis labels
    for (let i = axisMin; i <= axisMax; i += 5) {
        const posX = margin + (i - axisMin) * unit;
        ctx.fillText(i, posX, margin + gridSize + 15); // Below the plot
    }

    // Y-axis labels
    ctx.textAlign = 'right';
    for (let i = axisMin; i <= axisMax; i += 5) {
        const posY = margin + gridSize - (i - axisMin) * unit;
        ctx.fillText(i, margin - 10, posY); // Left of the plot
    }

    drawLegend();
}


function drawLegend() {
    const legendX = margin + gridSize + 20; // X position for the legend
    const legendY = margin; // Y position for the legend
    const legendSpacing = 20; // Spacing between legend items

    ctx.font = '12px Arial';
    ctx.textAlign = 'left';
    ctx.textBaseline = 'middle';

    let yOffset = legendY;

    for (const [label, color] of Object.entries(_label_to_color)) {
        // Draw color box
        ctx.fillStyle = color;
        ctx.fillRect(legendX, yOffset - 8, 20, 20); // Small square for color

        // Draw label text
        ctx.fillStyle = '#000';
        ctx.fillText(label, legendX + 30, yOffset);

        yOffset += legendSpacing; // Move down for the next legend item
    }
}

function addPoint(x, y, color, text, type) {
    points.push({ x, y, color, text });
    drawPoint(x, y, color, type); // Pass the index to distinguish the last point
}

function drawPoint(x, y, color, type) {
    const canvasX = margin + (x - axisMin) * unit;
    const canvasY = margin + gridSize - (y - axisMin) * unit;

    if (type === 'triangle') {
        // Draw triangle for the last point
        const size = 15; // Size of the triangle
        ctx.beginPath();
        ctx.moveTo(canvasX, canvasY - size); // Top point of the triangle
        ctx.lineTo(canvasX - size, canvasY + size); // Bottom-left point
        ctx.lineTo(canvasX + size, canvasY + size); // Bottom-right point
        ctx.closePath();

        ctx.fillStyle = color;
        ctx.fill();

        // Add border around triangle
        ctx.lineWidth = 5; // Set border width
        ctx.strokeStyle = 'deeppink'; // Set border color (you can change it)
        ctx.stroke();
    } else {
        // Draw circle for all other points
        ctx.beginPath();
        ctx.arc(canvasX, canvasY, 5, 0, 2 * Math.PI);
        ctx.fillStyle = color;
        ctx.fill();
        ctx.closePath();
    }
}

// Tooltip functionality when clicking on a point
canvas.addEventListener('click', (event) => {
    const rect = canvas.getBoundingClientRect();
    const mouseX = event.clientX - rect.left;
    const mouseY = event.clientY - rect.top;

    for (const point of points) {
        const canvasX = margin + (point.x - axisMin) * unit;
        const canvasY = margin + gridSize - (point.y - axisMin) * unit;

        const dx = mouseX - canvasX;
        const dy = mouseY - canvasY;
        const distance = Math.sqrt(dx * dx + dy * dy);

        if (distance <= 8) { // Adjust for triangle size
            tooltip.style.left = `${event.clientX + 10}px`;
            tooltip.style.top = `${event.clientY + 10}px`;
            tooltip.style.display = 'block';
            tooltip.textContent = point.text;
            return;
        }
    }

    tooltip.style.display = 'none';
});

// Initialize plot
drawPlot();
