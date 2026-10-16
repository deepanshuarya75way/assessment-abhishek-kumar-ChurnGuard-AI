const form = document.getElementById("predictionForm");
const predictButton = document.getElementById("predictButton");
const resultCard = document.getElementById("result");
const predictionText = document.getElementById("prediction");
const probabilityText = document.getElementById("probability");
const riskText = document.getElementById("risk");
const errorMessage = document.getElementById("errorMessage");

const feedbackRight = document.getElementById("feedbackRight")
const feedbackWrong = document.getElementById("feedbackWrong")
const feedbackMessage = document.getElementById("feedbackMessage")

let currentFeedback = null;
letfeedbackSubmitting = false;
function newPredictionId(){
    if(window.crypto && crypto.randomUUID){
        return crypto.randomUUID();
    }
    return "p-"+ Date.now().toString(36)+"-"+Math.random().toString(36).slice(2,10);
}
function resetFeedback(customer,data){
    currentFeedback = {
        prediction_id: newPredictionId(),
        customer_input:customer,
        prediction: data.prediction,
        churn_probability: data.churn_probability,
        risk_level: data.risk_level
    };
    feedbackSubmitting=false,
    feedbackRight.disabled =false,
    feedbackWrong.disabled =false,
    feedbackMessage.textContent="",
    feedbackMessage.className = "feedback-message"

}


form.addEventListener("submit", async function (event) {
    // Prevent the browser from refreshing the page
    event.preventDefault();

    errorMessage.textContent = "";
    resultCard.hidden = true;

    // Read all customer details from the form
    const formData = new FormData(form);
    const customer = {};

    for (const [key, value] of formData.entries()) {
        customer[key] = value;
    }

    // Convert numeric fields from text to numbers
    customer.SeniorCitizen = Number(customer.SeniorCitizen);
    customer.tenure = Number(customer.tenure);
    customer.MonthlyCharges = Number(customer.MonthlyCharges);
    customer.TotalCharges = Number(customer.TotalCharges);

    predictButton.disabled = true;
    predictButton.textContent = "Analyzing Customer...";

    try {
        // Send customer details to the FastAPI backend
        const response = await fetch("/api/predict", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(customer)
        });

        const data = await response.json();

        // Display backend validation or prediction errors
        if (!response.ok) {
            throw new Error(
                data.detail
                    ? JSON.stringify(data.detail)
                    : "Unable to predict customer churn."
            );
        }

        // Show prediction results
        predictionText.textContent =
            "Prediction: " + data.prediction;

        probabilityText.textContent =
            (data.churn_probability * 100).toFixed(2) + "%";

        riskText.textContent = data.risk_level;

        // Add simple risk-based colors
        if (data.risk_level === "High") {
            riskText.style.color = "#dc2626";
        } else if (data.risk_level === "Medium") {
            riskText.style.color = "#d97706";
        } else {
            riskText.style.color = "#16a34a";
        }
        resetFeedback(customer,data);
        resultCard.hidden = false;

        resultCard.hidden = false;

        // Scroll down to the prediction result
        resultCard.scrollIntoView({
            behavior: "smooth",
            block: "center"
        });

    } catch (error) {
        errorMessage.textContent =
            "Error: " + error.message;

    } finally {
        predictButton.disabled = false;
        predictButton.textContent = "Predict Customer Churn";
    }
});

async function sendFeedback(isCorrect){
    if(!currentFeedback || feedbackSubmitting){
        return;
    }
    feedbackSubmitting=true,
    feedbackRight.disabled =true,
    feedbackWrong.disabled =true,
    feedbackMessage.textContent="feedback message",
    feedbackMessage.className = "feedback saving"

    try{
        const response =await fetch("/feedback",{
            method:"POST",
            headers:{"Content-Type":"application/json"},
            body:JSON.stringify({...currentFeedback,is_correct:isCorrect})    
        });
        const body =await response.json().catch(()=>({}));

        if(response.ok || response.status===409){
            feedbackMessage.textContent =response.ok
                ? "good"+body.message
                : "! feedback already submitted";
            feedbackMessage.classList.add("success");
            return;     
        }
        throw new Error(body.detail || "could not save feedback");

    }catch(error){
        feedbackMessage.textContent=error.message+"please try again";
        feedbackMessage.classList.add("failure");
        feedbackSubmitting=false;
        feedbackRight.disabled =false;
        feedbackWrong.disabled = false;

    }

}
feedbackRight.addEventListener("click", () => sendFeedback(true));
feedbackWrong.addEventListener("click", () => sendFeedback(false));
