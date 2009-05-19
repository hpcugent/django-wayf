function CheckAll(cbName)
{
    for( i=0; i<document.firstForm.elements.length; i++) {
        if (document.firstForm.elements[i].name==cbName) {
            document.firstForm.elements[i].checked=document.firstForm.mc_select_all.checked;
        }
    }
}

function CheckPhoneNumber(val, msg) {
    str = new String(val);

    if (str.search(/^\+?[0-9]+$/) != -1) {
        return true;
    }

    alert(msg);
    return false;
}

function overlib_tooltip(msg) {
    return overlib(msg, CSSCLASS, FGCLASS, "ol_class_fg", BGCLASS, "ol_class_bg", TEXTFONTCLASS, "ol_class_fn", TIMEOUT, 5000, DELAY, 2000);
}

function fillCheckboxes(){
    for(i = 0; i < bigForm.elements.length; i++){
        if (bigForm.elements[i].name =='status' || bigForm.elements[i].name=='status_dropped')
            bigForm.elements[i].checked=true;
    }
}
function charsleft(f) {
    var a = f.value.length
    var ml = 159
    var l = document.forms["sendsms"]
    if (a>ml){f.value=f.value.substring(0,ml);charsleft(f);}
    l.num.value = a
  //l.numsms.value = Math.ceil( a / 160 )
}
function toggleVisibility( obj ) {
    var elm = document.getElementById(obj);
    if ( elm == null ) return;
    if( elm.style.visibility == 'visible' ) {
        elm.style.visibility = 'hidden';
        elm.style.display = 'none';
    } else {
        elm.style.visibility = 'visible';
        elm.style.display = 'block';
    }
}

function toggleSearchImage( obj , originalImagePath, newImagePath){
    var image1 = new Image();
    var image2 = new Image();
    image1.src = originalImagePath;
    image2.src = newImagePath;

    if( document.getElementById(obj).src == image1.src){
        document.getElementById(obj).src = image2.src ;
    } else {
        document.getElementById(obj).src = image1.src ;
    }
    /*if( document[ obj ].src == image1.src){
        document[ obj ].src = image2.src ;
    } else {
        document[ obj ].src = image1.src ;
    }
    */
    //alert('current image' + document[ obj ].src );
}

function toggleImage( obj ){
    var image1 = new Image();
    var image2 = new Image();
    image1.src = '../img/window_nofullscreen.png';
    image2.src = '../img/window_fullscreen.png';

    if( document[ obj ].src == image1.src){
        document[ obj ].src = image2.src ;
    } else {
        document[ obj ].src = image1.src ;
    }
}

function showHideFilter(l, imageName, origImagePath, newImagePath) {

    toggleSearchImage( imageName , origImagePath, newImagePath);
    
    var elm = document.getElementById(l);
    if( elm == null ) return;
    if( elm.style.display != 'block' ) {
        elm.style.display = 'block';
    } else {
        elm.style.display = 'none';
    }
    //var image = document.getElementById(imageName);

}


/** Used in User Role Group management. Guides the user, by only allowing the appropriate button to be clicked
 * depending on the select box the user has clicked on...
 *
 * @param clickedElemId     The id of the select box the user clicked on.
 * @param notClickedElemId  The id of the select box, where the user's current selection needs to be unselected.
 * @param buttonToDisableId The id of the button to disable and display as greyed out..
 * @param buttonToEnableId  The id of the button to enable and display properly. 
 */
function regulateSelections(clickedElemId, notClickedElemId, buttonToDisableId, buttonToEnableId){
    var clickedElem = document.getElementById(clickedElemId);
    var notClickedElem = document.getElementById(notClickedElemId);
    var buttonToDisable = document.getElementById(buttonToDisableId);
    var buttonToEnable = document.getElementById(buttonToEnableId);

    if(clickedElem && notClickedElem && buttonToDisable && buttonToEnable){
        notClickedElem.selectedIndex=-1;
        buttonToEnable.disabled='';
        buttonToDisable.disabled='disabled';

        if(buttonToEnable.className == 'addButton_disabled'){
            buttonToEnable.className='addButton_enabled';
        }else if (buttonToEnable.className == 'remButton_disabled'){
            buttonToEnable.className = 'remButton_enabled';
        }

        if(buttonToDisable.className == 'addButton_enabled'){
            buttonToDisable.className = 'addButton_disabled';
        }else if (buttonToDisable.className == 'remButton_enabled'){
            buttonToDisable.className = 'remButton_disabled';
        }



    }

}


   function smartOptionFinder(oSelect, oEvent, finderId, finderDivId) {

        var sKeyCode = oEvent.keyCode;

        var sToChar = String.fromCharCode(sKeyCode);
        var sTest;
        if (sKeyCode > 47 && sKeyCode < 91) {
        var sNow = new Date().getTime();
        if (oSelect.getAttribute("finder") == null) {
            oSelect.setAttribute("finder", sToChar.toUpperCase())
            oSelect.setAttribute("timer", sNow)
            toggleVisibility(finderDivId);
        } else if (sNow > parseInt(oSelect.getAttribute("timer")) + 2000) { //Reset all;
            oSelect.setAttribute("finder", sToChar.toUpperCase())
            oSelect.setAttribute("timer", sNow) //reset timer;
        } else {
            oSelect.setAttribute("finder", oSelect.getAttribute("finder") + sToChar.toUpperCase())
            oSelect.setAttribute("timer", sNow); //update timer;
        }
        var sFinder = oSelect.getAttribute("finder");
        var arrOpt = oSelect.options;
        var iLen = arrOpt.length;

        //first de-select all
        for (var j = 0; j < iLen; j++) {
            arrOpt[j].selected = false;
        }

        //now select appropriate...
        for (var i = 0; i < iLen; i++) {
            sTest = arrOpt[i].text;
            if (sTest.toUpperCase().indexOf(sFinder) >= 0) {
                arrOpt[i].selected = true;
            }
        }

        //set sFinder value in label, so that users know what they've put in...
        document.getElementById(finderId).innerHTML= sFinder;


        oEvent.returnValue = false;
        }// else {

       //}
    }
