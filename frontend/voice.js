const question = document.getElementById("question");
const speechResultField = document.getElementById("speech-result");
const questionResultField = document.getElementById("question-result");
let currentIndex = 0;
let detectionArray = []
let reportGenerated = false;
let screenshotTaken = false;  // Flag to ensure screenshot is only taken once


window.onload = () => {
    const content = document.getElementById('content');
    const image = document.getElementById('ok-img');
    const video = document.getElementById('webcam-video');
    const recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;

    const countdownText = document.createElement('div');
    countdownText.id = 'countdown-text';
    countdownText.style.position = 'absolute';
    countdownText.style.top = '50%';
    countdownText.style.left = '50%';
    countdownText.style.transform = 'translate(-50%, -50%)';
    countdownText.style.fontSize = '48px';
    countdownText.style.color = 'white';
    countdownText.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
    countdownText.style.padding = '10px';
    countdownText.style.borderRadius = '10px';
    countdownText.style.display = 'none'; // Hide initially
    countdownText.style.zIndex = '3'; // Ensure it's on top
    document.body.appendChild(countdownText);

    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(function (stream) {
                video.srcObject = stream;
                video.play();
            })
            .catch(function (error) {
                console.error("Error accessing webcam: ", error);
            });
    } else {
        console.warn("getUserMedia is not supported in this browser.");
    }

    let partsArray = [
        'Left Front Tire',
        'Right Front Tire',
        //'Left Rear Tire',
        //'Right Rear Tire',
        // 'Tire Summary',
        // 'Battery',
        // 'Battery Rust',
        // 'Battery Summary',
        // 'Exterior Rust',
        // 'Exterior Oil Leak',
        // 'Exterior Summary',
        // 'Brake Fluid Level',
        // 'Front Brake',
        // 'Rear Brake',
        // 'Emergency Brake',
        // 'Brake Summary',
        // 'Engine Rust',
        // 'Engine Oil',
        // 'Engine Oil Color',
        // 'Engine Fluid',
        // 'Engine Fluid Color',
        // 'Engine Oil Leak',
    ];

    function askNextQuestion() {
        if (currentIndex < partsArray.length) {
            question.innerText = `What is the condition of ${partsArray[currentIndex]}?`;
            questionResultField.value = partsArray[currentIndex];
        } else {
        }
        image.src = "";
        content.innerText = "";
        screenshotTaken = false;
    }

    // Start voice recognition automatically when the page loads
    recognition.start();
    askNextQuestion(); // Start asking questions immediately

    let isProcessing = false;  // Flag to ensure only one screenshot is captured at a time

    recognition.onresult = function (event) {
        let result = '';
        for (let i = event.resultIndex; i < event.results.length; i++) {
            result += event.results[i][0].transcript;

            content.innerText = result;
            speechResultField.value = result;
            if (!isProcessing && (event.results[i][0].transcript.trim().toLowerCase() === "ok" || event.results[i][0].transcript.trim().toLowerCase() === "okay")) {
                isProcessing = true;  // Prevent further detection during processing

                // Start the countdown before capturing the screenshot
                captureScreenshot(() => {
                    if (currentIndex < partsArray.length - 1) {
                        currentIndex++;
                        askNextQuestion();
                    }
                    else {
                        if (!reportGenerated) {
                            GenerateReport();
                            reportGenerated = true;
                        }
                    }
                    isProcessing = false;  // Allow further detection after processing is complete
                });
                break;
            }
            if (!isProcessing && (event.results[i][0].transcript.trim().toLowerCase() === "record" || event.results[i][0].transcript.trim().toLowerCase() === "no")) {
                isProcessing = true;  // Prevent further detection during processing

                // Start the countdown before recording the video
                startVideoRecording(() => {
                    if (currentIndex < partsArray.length - 1) {
                        currentIndex++;
                        askNextQuestion();
                    }
                    else {
                        if (!reportGenerated) {
                            GenerateReport();
                            reportGenerated = true;
                        }
                    }
                    isProcessing = false;  // Allow further detection after processing is complete
                });
                break;
            }
        }
        // if (currentIndex == partsArray.length - 1) {
        //                     GenerateReport();
        //                     reportGenerated = true;
        // }
    };

    recognition.onend = function () {
        // Restart recognition to keep it always active
        recognition.start();
    };

    function GenerateReport() {
        question.innerText = "All questions completed. Generating Report";
        console.log(detectionArray);

        // Prepare the payload (assuming detectionArray is already populated)
        let payload = detectionArray;

        // Send the payload to the Flask endpoint
        fetch('http://localhost:5000/generate_report', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Failed to generate report');
                }
                return response.blob();
            })
            .then(blob => {
                // Create a link element, use it to download the PDF, then remove it
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = 'maintenance_report.pdf';
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
                a.remove();
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }


    function captureScreenshot(callback) {
        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const ctx = canvas.getContext('2d');

        // Display the countdown text
        let seconds = 5; // Set delay to 5 seconds
        countdownText.style.display = 'block';
        countdownText.innerText = `Capturing image in ${seconds}...`;

        // Countdown timer
        let interval = setInterval(() => {
            seconds--;
            if (seconds > 0) {
                countdownText.innerText = `Capturing image in ${seconds}...`;
            } else {
                clearInterval(interval);
                countdownText.style.display = 'none';

                // After 5-second delay, capture the screenshot
                // Draw the video frame to the canvas
                ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

                // Optionally, overlay the question on the screenshot
                ctx.font = "24px Arial";
                ctx.fillStyle = "white";
                ctx.fillText(question.innerText, 20, 30);

                // Convert canvas to image data URL and store in detection array
                const dataUrl = canvas.toDataURL('image/png');
                detectionArray.push({ question: partsArray[currentIndex], image: dataUrl, status: "ok" });
                console.log("Screenshot captured and stored:", detectionArray);

                // Execute callback to move on to the next question
                callback();
            }
        }, 1000); // Update countdown every second
    }
    function startVideoRecording(callback) {
        // Display the countdown text
        let seconds = 30; // Set video recording duration to 30 seconds
        countdownText.style.display = 'block';
        countdownText.innerText = `Recording video for ${seconds} seconds...`;

        // Start recording the video
        if (video.srcObject) {
            mediaRecorder = new MediaRecorder(video.srcObject);
            mediaRecorder.ondataavailable = function (event) {
                if (event.data.size > 0) {
                    recordedChunks.push(event.data);
                }
            };

            mediaRecorder.onstop = function () {
                const blob = new Blob(recordedChunks, { type: 'video/webm' });
                const videoUrl = URL.createObjectURL(blob);
                detectionArray.push({ question: partsArray[currentIndex], video: videoUrla, status: "not ok" });
                console.log("Video recorded and stored:", detectionArray);

                // Clear the recorded chunks array for the next recording
                recordedChunks = [];

                // Execute callback to move on to the next question
                callback();
            };

            mediaRecorder.start();

            // Countdown timer for video recording
            let interval = setInterval(() => {
                seconds--;
                if (seconds > 0) {
                    countdownText.innerText = `Recording video for ${seconds} seconds...`;
                } else {
                    clearInterval(interval);
                    countdownText.style.display = 'none';
                    mediaRecorder.stop();  // Stop recording after 30 seconds
                }
            }, 1000); // Update countdown every second
        } else {
            console.error("No video stream available for recording.");
        }
    }

};

