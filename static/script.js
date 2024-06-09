/* static/script.js */
async function fetchTuningResults() {
    try {
        const response = await fetch('/tuning_results');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const tuningErrors = await response.json();

        if (!Array.isArray(tuningErrors)) {
            throw new Error('Invalid data format');
        }

        const loadingIndicator = document.getElementById('loading-indicator');
        loadingIndicator.style.display = 'none';

        tuningErrors.forEach(([stringName, tuningError]) => {
            const indicatorElement = document.getElementById(stringName).querySelector('.tuning-indicator');
            const absError = Math.abs(tuningError);
            const maxError = 10;

            let colorRatio = absError / maxError;
            if (tuningError > 0) {
                colorRatio = 1 - colorRatio;
            }

            const indicatorColor = `hsl(180, ${colorRatio * 100}%, 50%)`;
            indicatorElement.style.backgroundColor = indicatorColor;

            if (absError > maxError / 2) {
                indicatorElement.classList.add(tuningError > 0 ? 'too-high' : 'too-low');
            } else {
                indicatorElement.classList.remove('too-high', 'too-low');
            }
        });
    } catch (error) {
        console.error('Failed to fetch tuning results:', error);
    }
}








setInterval(fetchTuningResults, 1000);
