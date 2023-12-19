let mousePopupElem;

document.addEventListener('mouseover', e => {
    let popupHTML = e.target.dataset.mousepopup;
    if (!popupHTML)
    {
        return;
    }
    show_mouse_popup(popupHTML)
    let x = e.x + 10;
    let y = e.y + 10;
    mousePopupElem.style.left = x + 'px';
    mousePopupElem.style.top = y + 'px';
});

document.addEventListener('mouseout', e => {
    hide_mouse_popup()
});

function show_mouse_popup(text)
{
    hide_mouse_popup();
    mousePopupElem = document.createElement('div');
    mousePopupElem.className = 'mouse_popup';
    mousePopupElem.innerHTML = text;
    document.body.append(mousePopupElem);
}

function hide_mouse_popup()
{
    if (mousePopupElem)
    {
        mousePopupElem.remove();
        mousePopupElem = null;
    }
}