/*
Cross browser Marquee II- © Dynamic Drive (www.dynamicdrive.com)
For full source code, 100's more DHTML scripts, and TOS, visit http://www.dynamicdrive.com
Modified by jscheuer1 for continuous content. Credit MUST stay intact for use
*/
document.getElementById("menu-roll").onLoad = function() {
	if (document.getElementById('menu-roll')) {
	    // do stuff
		//Specify the marquee's width (in pixels)
		var marqueewidth="200px"
		//Specify the marquee's height
		var marqueeheight="150px"
		//Specify the marquee's marquee speed (larger is faster 1-10)
		var marqueespeed=1
		//Specify initial pause before scrolling in milliseconds
		var initPause=1000
		//Specify start with Full(1)or Empty(0) Marquee
		var full=1
		//Pause marquee onMousever (0=no. 1=yes)?
		var pauseit=1
		//Specify Break characters for IE as the two iterations
		//of the marquee, if text, will be too close together in IE
		var iebreak='<p></p>'

		//Specify the marquee's content
		//Keep all content on ONE line, and backslash any single quotations (ie: that\'s great):

		var marqueecontent=document.getElementById("menu-roll");

		////NO NEED TO EDIT BELOW THIS LINE////////////
		var copyspeed=marqueespeed
		var pausespeed=(pauseit==0)? copyspeed: 0
		var iedom=document.all||document.getElementById
		var actualheight=''
		var cross_marquee, cross_marquee2, ns_marquee

		function populate(){
			if (iedom){
			var lb=document.getElementById&&!document.all? '' : iebreak
			cross_marquee=document.getElementById? document.getElementById("iemarquee") : document.all.iemarquee
			cross_marquee2=document.getElementById? document.getElementById("iemarquee2") : document.all.iemarquee2
			cross_marquee.style.top=(full==1)? '8px' : parseInt(marqueeheight)+8+"px"
			cross_marquee2.innerHTML=cross_marquee.innerHTML=marqueecontent+lb
			actualheight=cross_marquee.offsetHeight
			cross_marquee2.style.top=(parseInt(cross_marquee.style.top)+actualheight+8)+"px" //indicates following #1
			}
			else if (document.layers){
			ns_marquee=document.ns_marquee.document.ns_marquee2
			ns_marquee.top=parseInt(marqueeheight)+8
			ns_marquee.document.write(marqueecontent)
			ns_marquee.document.close()
			actualheight=ns_marquee.document.height
			}
			setTimeout('lefttime=setInterval("scrollmarquee()",20)',initPause)
			}
			window.onload=populate

		function scrollmarquee(){

			if (iedom){
				if (parseInt(cross_marquee.style.top)<(actualheight*(-1)+8))
					cross_marquee.style.top=(parseInt(cross_marquee2.style.top)+actualheight+8)+"px"
				if (parseInt(cross_marquee2.style.top)<(actualheight*(-1)+8))
					cross_marquee2.style.top=(parseInt(cross_marquee.style.top)+actualheight+8)+"px"
					cross_marquee2.style.top=parseInt(cross_marquee2.style.top)-copyspeed+"px"
					cross_marquee.style.top=parseInt(cross_marquee.style.top)-copyspeed+"px"
				}
				else if (document.layers){
					if (ns_marquee.top>(actualheight*(-1)+8))
						ns_marquee.top-=copyspeed
						else
						ns_marquee.top=parseInt(marqueeheight)+8
					}
			}

			if (iedom||document.layers){
				with (document){
				if (iedom){
				write('<div style="position:relative;width:'+marqueewidth+';height:'+marqueeheight+';overflow:hidden" onMouseover="copyspeed=pausespeed" onMouseout="copyspeed=marqueespeed">')
				write('<div id="iemarquee" style="position:absolute;left:0px;top:0px;width:100%;">')
				write('</div><div id="iemarquee2" style="position:absolute;left:0px;top:0px;width:100%;z-index:100;background:white;">')
				write('</div></div>')

				}
				else if (document.layers){
				write('<ilayer width='+marqueewidth+' height='+marqueeheight+' name="ns_marquee">')
				write('<layer name="ns_marquee2" width='+marqueewidth+' height='+marqueeheight+' left=0 top=0 onMouseover="copyspeed=pausespeed" onMouseout="copyspeed=marqueespeed"></layer>')
				write('</ilayer>')
				}
			}
		}
	} else {
    	setTimeout(myFunc, 15);
  	}
};