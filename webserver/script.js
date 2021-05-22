var url ="http://" + window.location.hostname + ":5000/"
var urlAuth = "http://" + "0.0.0.0" + ":5555/"
var urlProdus = url + 'products'
var urlComenzi = url +'orders'
var urlLogin = urlAuth + 'login'
var urlLogout = urlAuth + 'logout'
var urlIngr = url + 'ingredients'
var urlSignUp = url + 'users'
var urlTabelProdus = url + 'filter_products'
var urlTabelComenzi = url + 'filter_orders'

var urlGraficIngredient = url + 'group_products_ingr'
var urlGraficCategorie = url + 'group_products_categ'
var arrayFiltrare = [];
var arrayProduse = [];

var categorieSelectata;
var ingredientPrincipalSelectat;

var anSelectat;
var lunaSelectata;
var ziSelectata;
var pretSelectat;

var ingredientPrincipal;
var selectProdus;
var isAdmin;

$(document).ready(function () {



  if(localStorage.getItem('isAdmin') == 1){
    $('#butonRedirectCreareProdus').css({'display':'block !important'});
    $('#butonRedirectCreareIngredient').css({'display':'block !important'});
  }
  else {
    $('#butonRedirectCreareProdus').css({'display':'none'});
    $('#butonRedirectCreareIngredient').css({'display':'none'});
  }

  $.get(urlProdus, function (data, status) {
    //console.log( "Sample of data:", data );
    console.log("Data: " + data + "\nStatus: " + status);
    selectProdus = document.getElementById('selectProdus');
    produse = (JSON.parse(data))['data'];
    for (var produs of produse){
      $('#produse').append('<div class="card" style="min-width:500px; min-height:250px; margin:15px; background: #eee;">' +
        '<div class="card-body"><h5 class="card-title">' + produs.NAME + '</h5>' +
        '<p class="card-text"><span style="font-weight:bolder">Main Ingredient: </span><span style="margin-left: 10px;">' + produs.MAIN_INGREDIENT + '</p>' +
        '<p class="card-text"><span style="font-weight:bolder">Description: </span><span style="margin-left: 10px;">' + produs.DESCRIPTION + '</p>' +
        '<p class="card-text"><span style="font-weight:bolder">Price:</span><span style="margin-left: 10px;">' + produs.PRICE + '</span> LEI</p>' +       
        '<p class="card-text"><span style="font-weight:bolder">Measure Unit: </span><span style="margin-left: 10px;">' + produs.MEASURE_UNIT + '</p>' +
        '<p class="card-text"><span style="font-weight:bolder">Category: </span><span style="margin-left: 10px;">' + produs.CATEGORY + '</p>' +
        ' </div> </div></br></br>');
      if(selectProdus != null)
        selectProdus.options.add( new Option(produs.NAME, produs.ID_PRODUCT) )
    }
  });

  $.get(urlComenzi + '/' + localStorage.getItem('token'), function (data, status) {
    //console.log( "Sample of data:", data );
    console.log("Data: " + data + "\nStatus: " + status);

    comenzi = (JSON.parse(data))['data'];
    for (var comanda of comenzi)
      $('#comenzi').append('<div class="card" style="min-width:500px; min-height:250px; margin:15px; background: #eee;">' +
        '<div class="card-body"><h5 class="card-title">' + comanda.ID_ORDER + '</h5>' +
        '<p class="card-text"><span style="font-weight:bolder">Date of the order: </span><span style="margin-left: 10px;">' + comanda.ORDER_DATE + '</p>' +
        '<p class="card-text"><span style="font-weight:bolder">Client: </span><span style="margin-left: 10px;">' + comanda.USER_NAME + '</p>' +
        '<p class="card-text"><span style="font-weight:bolder">Total Price: </span><span style="margin-left: 10px;">' + comanda.PRICE + '</span> RON</p>' +  
        '<p class="card-text"><span style="font-weight:bolder">Product Name: </span><span style="margin-left: 10px;">' + comanda.PRODUCT_NAME + '</p>' +   
        '<p class="card-text"><span style="font-weight:bolder">Product Category: </span><span style="margin-left: 10px;">' + comanda.PRODUCT_CATEGORY + '</p>' +   
        //'<p class="card-text">Cantitate: <span style="margin-left: 10px;">' + comanda.CANTITATE + '</p>' +
        ' </div> </div></br></br>');
  });

  $.get(urlIngr, function (data, status) {
    //console.log( "Sample of data:", data );
    console.log("Data: " + data + "\nStatus: " + status);
    ingredientPrincipal = document.getElementById('ingredientPrincipal');

    ingrediente = (JSON.parse(data))['data'];
    for (var ingr of ingrediente) {
      $('#ingrediente').append('<div class="card" style="min-width:250px; min-height:150px; margin:15px; background: #eee;">' +
        '<div class="card-body"><h5 class="card-title">' + "INGREDIENT" + '</h5>' +
        '<p class="card-text"><span class="cardDenumire">Name: </span> <span style="margin-left: 10px;">' + ingr.NAME + '</p>' +
        ' </div> </div></br></br>');
      if(ingredientPrincipal != null)
        ingredientPrincipal.options.add( new Option(ingr.NAME, ingr.ID_INGREDIENT) ) 
    }
  });

  $('#login').click(function() {
    var credentials = {EMAIL: $('#inputEmail').val(), PASSWORD: $('#inputPassword').val() };
    console.log(credentials)
    $.ajax({
      type: "POST",
      url: urlLogin,
      contentType: "application/json; charset=utf-8",
      dataType: "JSON",
      data: JSON.stringify(credentials),
      success: function(result){
       console.log(result)
       if(result.status == 200){
        localStorage.setItem('token', result.TOKEN);
        localStorage.setItem('isAdmin', result.IS_ADMIN);
        token = result.TOKEN;
        isAdmin = result.IS_ADMIN;
        location.href = "index.html";
      }



      else 
        alert('Incorrect Credentials!')
    }
  });
  });

  $('#butonLogout').on('click', function() {
    var body = {TOKEN: localStorage.getItem('token')};
    console.log(body)
    $.ajax({
      type: "POST",
      url: urlLogout + '/' + localStorage.getItem('token'),
      contentType: "application/json; charset=utf-8",
      dataType: "JSON",
      data: [],
      success: function(result){
       console.log(result)

       localStorage.removeItem('token');
       location.href = "login.html";
     }
   });
  });

  $('#butonSignup').click(function() {
    var informatii = {
      SURNAME: $('#inputNume').val(),
      FORENAME: $('#inputPrenume').val(),
      EMAIL: $('#inputEmail2').val(),
      PHONE: $('#inputTelefon').val(),
      ADDRESS: $('#inputAdresa').val(),
      PASSWORD: $('#inputPassword2').val(),
      IS_ADMIN: 0
    };
    console.log(informatii)
    console.log(urlSignUp)

    $.ajax({
      type: "POST",
      url: urlSignUp,
      contentType: "application/json; charset=utf-8",
      dataType: "JSON",
      data: JSON.stringify(informatii),
      success: function(result){
       console.log(result)
       if(result.status == 200){
        localStorage.setItem('token', result.TOKEN);
        token = result.TOKEN;
        location.href = "index.html";
      }

      else 
        alert('Incorrect Credentials!')
    }
  });
  });

  $('#butonAdaugaProdus').click(function() {
    var informatii = {
      NAME: $('#inputDenumire').val(),
      DESCRIPTION: $('#descriere').val(),
      MAIN_INGREDIENT: $('#ingredientPrincipal')[0].value,
      MEASURE_UNIT: $('#inlineGramaj')[0].checked ? 'weight' : 'piece',
      PRICE: $('#inputPretUnitar').val(),
      CATEGORY: $('#categorie')[0].value
    };
    console.log(informatii)

    $.ajax({
      type: "POST",
      url: urlProdus,
      contentType: "application/json; charset=utf-8",
      dataType: "JSON",
      data: JSON.stringify(informatii),
      success: function(result){
       console.log(result)
       if(result.status == 200){
        location.href = "produse.html";
      }
    }
  })
  });

  $('#butonRedirectCreareProdus').on('click', function() {
    location.href = "creareProdus.html";
  })

  $('#butonRedirectCreareComanda').on('click', function() {
    location.href = "creareComanda.html";
  })

  $('#butonRedirectCreareIngredient').on('click', function() {
    location.href = "creareIngredient.html";
  })

  $('#butonAdaugaComanda').click(function() {
    var informatii = {
      TOKEN: localStorage.getItem('token'),
      QUANTITY: $('#inputCantitate').val(),
      ID_PRODUCT: $('#selectProdus')[0].value
    };

    console.log(informatii)

    $.ajax({
      type: "POST",
      url: urlComenzi,
      contentType: "application/json; charset=utf-8",
      dataType: "JSON",
      data: JSON.stringify(informatii),
      success: function(result){
       console.log(result)
       if(result.status == 200){
        location.href = "comenzi.html";
      }
    }
  })
  });

  $('#butonAdaugaIngredient').click(function() {
    var informatii = {
      NAME: $('#inputDenumire').val()
    };
    console.log(informatii)

    $.ajax({
      type: "POST",
      url: urlIngr,
      contentType: "application/json; charset=utf-8",
      dataType: "JSON",
      data: JSON.stringify(informatii),
      success: function(result){
       console.log(result)
       if(result.status == 200){
        location.href = "ingrediente.html";
      }
    }
  })
  });

  $('#atributFiltrare').on('change', function () {
    console.log(this.value);
    if(this.value == 'categorie')
      getGraficCategorie();
    else {
      if(this.value == 'ingredient')
        getGraficIngredient();
    }
  });

  $('#butonProduse').click(function() {
    location.href = 'raportProdus.html';
    });

    $('#butonComanda').click(function() {
      location.href ='raportComenzi.html';
    });


$('#categ').on('change', function () {
    console.log(this.value);
    categorieSelectata = this.value;
  });

$('#ingredientPrincipal').on('change', function () {
    console.log(this.value);
    ingredientPrincipalSelectat = this.value;
  });

    $('#genereazaTabel').on('click', function () {
      if(categorieSelectata == undefined)
        categorieSelectata = "";
      if(ingredientPrincipalSelectat == undefined)
        ingredientPrincipalSelectat = 0;

      var info = {CATEGORY: categorieSelectata, INGREDIENT: ingredientPrincipalSelectat};
      console.log(info);
      $.ajax({
      type: "POST",
      url: urlTabelProdus,
      contentType: "application/json; charset=utf-8",
      dataType: "JSON",
      data: JSON.stringify(info),
      success: function(result){
       console.log(result)
       if(result.status == 200){
        var produseAfiste = result.data
        console.log(produseAfiste)
        if(produseAfiste.length > 0) {
        $('#tabelInfo').empty();

        //adaugam head-ul
        $('#tabelInfo').append('<thead> \
    <tr  style="background: #ea873dd6; color:white;">\
      <th scope="col">#</th>\
      <th scope="col">Name</th>\
      <th scope="col">Price</th>\
      <th scope="col">Measure Unit</th>\
      <th scope="col">Category</th>\
      <th scope="col">Main Ingredinet</th>\
    </tr>\
  </thead>');
        
        //pentru fiecare element din vecorul de elemente 
        for(var i = 0; i< produseAfiste.length; i++) {

            //adaugam la sfarsitul tabelului un rand
            var inregistrare = document.getElementById("tabelInfo").insertRow(-1);

            var id = inregistrare.insertCell(0);
            var denumire = inregistrare.insertCell(1);
            var pret = inregistrare.insertCell(2);
            var unitateMasura = inregistrare.insertCell(3);
            var categorie = inregistrare.insertCell(4);
            var ingredient = inregistrare.insertCell(5);

            id.innerHTML = produseAfiste[i].ID_PRODUCT;
            denumire.innerHTML = produseAfiste[i].NAME;
            pret.innerHTML = produseAfiste[i].PRICE;
            unitateMasura.innerHTML = produseAfiste[i].MEASURE_UNIT;
            categorie.innerHTML = produseAfiste[i].CATEGORY;
            ingredient.innerHTML = produseAfiste[i].MAIN_INGREDIENT;
    };
}
      }
    }
  })

     
});

  $('#an').on('change', function () {
    console.log(this.value);
    anSelectat = this.value;
  });

  $('#luna').on('change', function () {
    console.log(this.value);
    lunaSelectata = this.value;
  });  

  $('#zi').on('change', function () {
    console.log(this.value);
    ziSelectata = this.value;
  });

  $('#inputPret').on('change', function () {
    console.log(this.value);
    pretSelectat = this.value;
  });

    $('#genereazaTabel2').on('click', function () {
      var DataSelectata = '';
      if(anSelectat != undefined && lunaSelectata != undefined && ziSelectata != undefined)
        DataSelectata = anSelectat + '-' + lunaSelectata + '-' + ziSelectata;

      if(pretSelectat == undefined)
        pretSelectat = -1;

      var info = {ORDER_DATE: DataSelectata, PRICE: pretSelectat};
      console.log(info);
      $.ajax({
      type: "POST",
      url: urlTabelComenzi,
      contentType: "application/json; charset=utf-8",
      dataType: "JSON",
      data: JSON.stringify(info),
      success: function(result){
       console.log(result)
       if(result.status == 200){
        var produseAfiste = result.data
        console.log(produseAfiste)
        if(produseAfiste != undefined) {
        $('#tabelInfo2').empty();

        //adaugam head-ul
        $('#tabelInfo2').append('<thead> \
    <tr  style="background: #ea873dd6; color:white;">\
      <th scope="col">#</th>\
      <th scope="col">Order Date</th>\
      <th scope="col">Client</th>\
      <th scope="col">Product</th>\
      <th scope="col">Price</th>\
    </tr>\
  </thead>');
        
        //pentru fiecare element din vecorul de elemente 
        for(var i = 0; i< produseAfiste.length; i++) {

            //adaugam la sfarsitul tabelului un rand
            var inregistrare = document.getElementById("tabelInfo2").insertRow(-1);

            var id = inregistrare.insertCell(0);
            var data = inregistrare.insertCell(1);
            var client = inregistrare.insertCell(2);
            var produs = inregistrare.insertCell(3);
            var pret = inregistrare.insertCell(4);

            id.innerHTML = produseAfiste[i].ID_ORDER;
            data.innerHTML = produseAfiste[i].ORDER_DATE;
            client.innerHTML = produseAfiste[i].USER_NAME;
            produs.innerHTML = produseAfiste[i].PRODUCT_NAME;
            pret.innerHTML = produseAfiste[i].PRICE;
    };
}
      }
    }
  })

     
});
});

function getGraficCategorie() {
  $.get(urlGraficCategorie, function (data, status) {
    arrayFiltrare = [];
    arrayProduse = [];
    //console.log( "Sample of data:", data );
    console.log("Data: " + data + "\nStatus: " + status);
    produse = (JSON.parse(data))['data'];
    for (var produs of produse){
      arrayFiltrare.push(produs.CATEGORY);
      arrayProduse.push(produs.NR_PROD);
    }
    desenareGrafic(arrayFiltrare, arrayProduse);
  });
}

function getGraficIngredient() {
  $.get(urlGraficIngredient, function (data, status) {
    arrayFiltrare = [];
    arrayProduse = [];
    //console.log( "Sample of data:", data );
    console.log("Data: " + data + "\nStatus: " + status);
    produse = (JSON.parse(data))['data'];
    for (var produs of produse){
      arrayFiltrare.push(produs.NAME);
      arrayProduse.push(produs.NR_PROD);
    }
    desenareGrafic(arrayFiltrare, arrayProduse);
  });

}

function desenareGrafic(arrayFiltrare, arrayProduse) {
 if($('canvas') != null)
  $('canvas').remove();

    //creare canvas
    var canvas = document.createElement("canvas"); console.log(canvas)
    var ctx = canvas.getContext("2d");

    //setare inaltime si lungime dorita
    canvas.width = 1200;
    canvas.height = 700;

    //il adugam la locul specific din html
    $(canvas).appendTo($('#divGrafic'));

    var myChart = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: arrayFiltrare,
        datasets: [{
          label: 'Products Number',
          data: arrayProduse,
          backgroundColor: [
          'rgba(255, 99, 132, 0.2)',
          'rgba(54, 162, 235, 0.2)',
          'rgba(255, 206, 86, 0.2)',
          'rgba(75, 192, 192, 0.2)',
          'rgba(153, 102, 255, 0.2)',
          'rgba(255, 159, 64, 0.2)'
          ],
          borderColor: [
          'rgba(255, 99, 132, 1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)',
          'rgba(75, 192, 192, 1)',
          'rgba(153, 102, 255, 1)',
          'rgba(255, 159, 64, 1)'
          ],
          borderWidth: 1
        }]
      },
      options: {
        legend: {
            display: false,
         },
        scales: {
          xAxes: [{
            gridLines: {
              color: 'rgba(171,171,171,1)',
              lineWidth: 1
            },
              ticks: {
                      fontColor : 'rgba(255,255,255,1)'}

          }],
          yAxes: [{
            ticks: {
              beginAtZero: true,
                fontColor : 'rgba(255,255,255,1)'
            },
            gridLines: {
              color: 'rgba(255,255,255,1)',
              lineWidth: 0.5
            }
          }]
        }
      }
    });
  }