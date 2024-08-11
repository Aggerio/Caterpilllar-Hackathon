window.onload = () => {
    const video = document.getElementById('webcam-video');
    const userDetails = document.getElementById('user-details');
    const canvas = document.createElement('canvas');
    const context = canvas.getContext('2d');
    const captureBtn = document.getElementById('capture-btn');

    // Access the webcam
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

    // Capture the current frame when the button is clicked
    captureBtn.addEventListener('click', () => {
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        context.drawImage(video, 0, 0, canvas.width, canvas.height);

        // Convert canvas to a Blob (PNG image)
        canvas.toBlob((blob) => {
            // Create a FormData object to send the file
            const formData = new FormData();
            formData.append('file', blob, 'qr_image.png');

            // Send the image to the Flask server
            fetch('http://localhost:5000/customer_details', {
                method: 'POST',
                body: formData,
            })
                .then(response => response.json())
                .then(customerData => {
                    userDetails.innerHTML = `
                    <h3>Customer Details</h3>
                    <p><strong>Customer Name:</strong> ${customerData.customer_name}</p>
                    <p><strong>Contact Name:</strong> ${customerData.contact_name}</p>
                    <p><strong>Contact Phone:</strong> ${customerData.contact_phone}</p>
                    <p><strong>Contact Email:</strong> ${customerData.contact_email}</p>
                    <p><strong>Address:</strong> ${customerData.customer_address}</p>
                    <p><strong>Machine:</strong> ${customerData.customer_machine}</p>
                    <p><strong>Serial Number:</strong> ${customerData.machine_serial_number}</p>
                    <p><strong>Machine Weight (tons):</strong> ${customerData.machine_weight_tons}</p>
                    <p><strong>Purchase Date:</strong> ${customerData.purchase_date}</p>
                    <p><strong>Last Service Date:</strong> ${customerData.last_service_date}</p>
                    <p><strong>Service Plan:</strong> ${customerData.service_plan}</p>
                    <p><strong>Warranty Expiration:</strong> ${customerData.warranty_expiration}</p>
                    <p><strong>ID:</strong> ${customerData.id}</p>
                    `;
                    //console.log(data);
                    const divToRemove = document.getElementById('qr-text');
                    if (divToRemove) {
                        divToRemove.remove();
                    }
                    captureBtn.innerHTML = 'Moving to Checkup';
                    captureBtn.disabled = true;

                    setTimeout(() => {
                        window.location.href = 'questionnaire.html';
                    }, 2000); // 2-second delay before redirecting

                })
                .catch(error => {
                    console.error('Error:', error);
                });
        }, 'image/png');
    });
};

