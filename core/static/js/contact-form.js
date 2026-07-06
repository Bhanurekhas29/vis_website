/* ==========================================================================
   Contact form — restricts Name to letters/spaces only, Mobile to
   digits only, blocking invalid keystrokes as the user types.
   ========================================================================== */

document.addEventListener("DOMContentLoaded", function () {
  var nameField = document.getElementById("id_name");
  var phoneField = document.getElementById("id_phone");

  if (nameField) {
    nameField.addEventListener("input", function () {
      this.value = this.value.replace(/[^A-Za-z\s]/g, "");
    });
  }

  if (phoneField) {
    phoneField.addEventListener("input", function () {
      this.value = this.value.replace(/[^0-9]/g, "").slice(0, 10);
    });
  }
});