// Get Stripe publishable key
fetch("/payments/config/")
.then((result) => { return result.json(); })
.then((data) => {
  // Initialize Stripe.js
  const stripe = Stripe(data.publicKey);
  const mode = document.querySelector('input[name="mode"]');

  function checkout(item_name) {
    // Get Checkout Session ID
    fetch("/payments/create-checkout-session/",{
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        item_name: item_name,
        mode: mode.value,
      })
    })
    .then((result) => { return result.json(); })
    .then((data) => {
      console.log(data);
      // Redirect to Stripe Checkout
      return stripe.redirectToCheckout({sessionId: data.sessionId})
    })
    .then((res) => {
      console.log(res);
    });
  }

  // Event handler
  // document.querySelector("#submit1").addEventListener("click", () => {
  //   free();
  // });
  document.querySelector("#submit2").addEventListener("click", () => {
    checkout("1 Month");
  });
  document.querySelector("#submit3").addEventListener("click", () => {
    checkout("1 Year");
  });
  document.querySelector("#submit4").addEventListener("click", () => {
    checkout("3 Years");
  });
});