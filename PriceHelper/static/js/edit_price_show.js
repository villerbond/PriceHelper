function show_edit(userProductId, userShopId) {
    var editForm = document.getElementById("edit-form-" + userProductId + "-" + userShopId);
    var editBtn = document.getElementById("edit-btn-" + userProductId + "-" + userShopId);
    editForm.removeAttribute('hidden');
    editBtn.setAttribute('hidden', 'true');
}

function hide_edit(userProductId, userShopId) {
    var editForm = document.getElementById("edit-form-" + userProductId + "-" + userShopId);
    var editBtn = document.getElementById("edit-btn-" + userProductId + "-" + userShopId);
    editForm.setAttribute('hidden', 'true');
    editBtn.removeAttribute('hidden');
}