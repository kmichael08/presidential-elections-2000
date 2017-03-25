$(function($) {

  var mapUrl = '';	/* ścieżka do pliku .png;
				   jeżeli mapa nie ładuje się poprawnie zamień na bezpośrednie odwołanie do pliku, np:
				   var mapUrl='http://example.com/map/pl-500px.png'; 
				   domyślnie ścieżka pobierana jest z pliku CSS, ale w niektórych przypadkach nie ładuje się prawidłowo */
  var loadingText = "Loading ..."; // tekst wyświetlany podczas ładowania mapy
  var loadingErrorText = "Brak mapy!"; // tekst błędu; wyświetlany, gdy nie został załadowany plik .png
  var tooltipArrowHeight = 6;	/* wysokość strzałki pod 'dymkiem' z nazwą regionu;
						   strzałkę możesz usunąć w pliku CSS, po usunięciu strzałki ustaw: var tooltipArrowHeight=0; */
  var visibleListId = '#map-widoczna-lista'; /* id div.a z widoczną listą regionów
    									  nie zapomnij o znaku hash (#)
    									  nie zapomnij zmienić id w pliku .css */
  var agentsListId = '#adresy';	/* id div.a z listą adresów/przedstawicieli
							   nie zapomnij o znaku hash (#)  */

  // TRYB WIELOKROTNEGO WYBORU (MULTIPLE-CLICK)
  var searchLink = 'szukaj.php'; // odnośnik do wyszukiwarki
  var searchLinkVar = 'wojewodztwo'; // zmienna przekazywana do skryptu wyszukiwarki
  var searchName = 'Szukaj'; // tekst odnośnika do wyszukiwarki


  $.multipleClickAction = function(e){
    var clickedRegions=[];
    $('#polska').find('.active-region').each(function(){ // szuka wybranych regionów (NIE EDYTUJ!)
       var url=$(this).children('a').attr('href'); // pobiera odnośniki wybranych regionów (NIE EDYTUJ!)

       // operacje na linkach

       var slicedUrl=url.slice(1); // domyślnie odcina hash (#) w odnośniku
       /* jeżeli użyjesz bezpiecznych odnośników, np: 'szukaj.php?wojewodztwo=mazowieckie'
          musisz 'odciąć' także parametry odnośnika:

          var slicedUrl=url.slice(url.indexOf('?')+13); // usuwa: '?wojewodztwo=' ... +13 to ilość odciętych znaków
       */

       // uzupełnia tablicę wybranymi regionami (NIE EDYTUJ!)
       clickedRegions.push(slicedUrl);
    });

    // tworzy odnośnik do wyszukiwarki wraz z zaznaczonymi regionami
    $('#search-link').attr('href',searchLink+'?'+searchLinkVar+'='+clickedRegions.join('|'));

   }

    // FUNKCJE STANDARDOWE
    // kliknięcie w region
    $.defaultClickAction = function(e) {
        // pobiera adres odnośnika klikniętego regionu (NIE EDYTUJ!)
        var url = $(e).children('a').attr('href'); 
        // domyślnie kliknięcie w region przenosi na stronę w odnośniku
        window.location.href = url;

        // wyświetla adres przedstawiciela w wybranym regionie
        $(agentsListId).find('li').hide();
        $(url+','+url+' li').show();
    }

    // ponowne kliknięcie w zaznaczony region
    $.doubleClickedRegion = function(e) {
        // domyślnie deaktywuje zaznaczony region
        $(e).removeClass('active-region');

        // ukrywa adresy przedstawicieli
        $(agentsListId).find('li').hide();
    }


/* --------------------------------------------------------
tutaj zaczyna sie mapa

NIE EDYTUJ! 

Polska, interaktywna mapa województw | http://winstonwolf.pl/clickable-maps/polska.html
script version: 3.4 by Winston Wolf | http://winstonwolf.pl
Copyright (C) 2011 Winston_Wolf | All rights reserved


poważnie, NIE EDYTUJ TEGO! */
$('#map-pl').prepend('<span id="loader">'+loadingText+'</span>').addClass('script');$('#polska').find('a').hide();$(agentsListId).find('li').hide();if($('#map-pl').hasClass('multiple-click')){if(searchLink==''){var searchLink='search.php';}
if(searchLinkVar==''){var searchLinkVar='region';} if(searchName==''){var searchName='Search';} $('<a href="'+searchLink+'" id="search-link">'+searchName+'</a>').insertAfter('#polska');} if($('#map-pl').hasClass('widoczna-lista')){$('#map-pl').after('<div id="'+visibleListId.slice(1)+'"><ul></ul></div>');} if(mapUrl==''){var mapUrl=$('#polska').css('background-image').replace(/^url\("?([^\"\))]+)"?\)$/i,'$1');}
var mapImg=new Image();$(mapImg).load(function(){var countRegions=0;var clickedRegions=[];$('#loader').fadeOut();$('#polska').find('li').each(function(){var liid=$(this).attr('id');var url=$(this).children('a').attr('href');var code=null;var spans=0;countRegions++;switch(liid){case'pl6':case'pl8':case'pl13':case'pl16':spans=26;break;case'pl5':case'pl7':case'pl15':spans=47;break;default:spans=31;}
var tooltipLeft=$(this).children('a').outerWidth()/-2;var tooltipTop=$(this).children('a').outerHeight()*-1-tooltipArrowHeight;if($('#map-pl').hasClass('no-tooltip')){var tooltipTop=0;}
$(this).prepend('<span class="map" />').append('<span class="bg" />').attr('tabindex',countRegions);for(var i=1;i<spans;i++){$(this).find('.map').append('<span class="s'+i+'" />');}
$(this).children('a').css({'margin-left':tooltipLeft,'margin-top':tooltipTop});if($('#map-pl').hasClass('widoczna-lista')){var liHref=$(this).children('a').attr('href');var liText=$(this).children('a').text();$(visibleListId+' ul').append('<li class="'+liid+'"><a href="'+liHref+'">'+liText+'</a></li>');}
if($(this).children('a').hasClass('active-region')||url==window.location.hash){$(this).addClass('active-region focus');$(agentsListId).find('li').hide();$(url+','+url+' li').show();$('.'+$(this).attr('id')).children('a').addClass('active-region');$('#search-link').attr('href',searchLink+'?'+searchLinkVar+'='+url.slice(1));}}).hover(function(){$.MapHoveredRegion($(this));},function(){$.MapUnHoveredRegion($(this));}).focus(function(){$.MapHoveredRegion($(this));}).blur(function(){$.MapUnHoveredRegion($(this));}).keypress(function(e){code=(e.keyCode?e.keyCode:e.which);if(code==13)$.MapClickedRegion($(this));}).click(function(e){$.MapClickedRegion($(this));});if($('#map-pl').hasClass('widoczna-lista')){$(visibleListId).find('a').each(function(){var itemId='#'+$(this).parent().attr('class');$(this).hover(function(){$.MapHoveredRegion(itemId);},function(){$.MapUnHoveredRegion(itemId);}).focus(function(){$.MapHoveredRegion(itemId);}).blur(function(){$.MapUnHoveredRegion(itemId);}).keypress(function(e){code=(e.keyCode?e.keyCode:e.which);if(code==13)$.MapClickedRegion(itemId);}).click(function(e){$.MapClickedRegion(itemId);});});}}).error(function(){$('#loader').text(loadingErrorText);$('#polska').find('span').hide();$('#map-pl,#polska').css({'height':'auto','left':'0','margin':'0 auto'});}).attr('src',mapUrl);$.MapClickedRegion=function(e){var listItemId='.'+$(e).attr('id');if($('#map-pl').hasClass('multiple-click')){if($(e).hasClass('active-region')){$(e).removeClass('active-region');$(listItemId).children('a').removeClass('active-region');}else{$(e).addClass('active-region');$(listItemId).children('a').addClass('active-region');}
$.multipleClickAction(e);}else{if($(e).hasClass('active-region')){$.doubleClickedRegion(e);$(listItemId).children('a').removeClass('active-region');window.location.hash="";}else{$('#polska,'+visibleListId).find('.active-region').removeClass('active-region');$('#polska').find('.focus').removeClass('focus');if($(e).hasClass('active-region')){$(e).removeClass('active-region focus');$(listItemId).children('a').removeClass('active-region');}else{$(e).addClass('active-region focus').children('a').show();$(listItemId).children('a').addClass('active-region');}
$.defaultClickAction(e);}}}
$.MapHoveredRegion=function(e){$('#polska').find('.active-region').children('a').hide();$(e).children('a').show();$(e).addClass('focus');$('.'+$(e).attr('id')).children('a').addClass('focus');}
$.MapUnHoveredRegion=function(e){$(e).children('a').hide();if($(e).hasClass('active-region')==false){$(e).removeClass('focus');} $('.'+$(e).attr('id')).children('a').removeClass('focus');}
var loaderLeft=$('#loader').outerWidth()/-2;var loaderTop=$('#loader').outerHeight()/-2;$('#loader').css({'margin-left':loaderLeft,'margin-top':loaderTop});
// koniec mapy

});