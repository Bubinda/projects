var productModal = $("#productModal");
    $(function () {

        //JSON data by API call
        $.get(productListApiUrl, function (response) {
            if(response) {
                var table = '';
                $.each(response, function(index, product) {
                    table += '<tr data-id="'+ product.product_id +'" data-name="'+ product.name +'" data-unit="'+ product.unit_id +'" data-price="'+ product.price_per_unit +'">' +
                        '<td>'+ product.name +'</td>'+
                        '<td>'+ product.unit_name +'</td>'+
                        '<td>'+ product.price_per_unit +'</td>'+
                        '<td><span class="btn btn-xs btn-danger delete-product">Delete</span></td></tr>';
                });
                $("table").find('tbody').empty().html(table);
            }
        });
    });


    // $(document).on("click", ".add-product", function (){
    //     productModal.modal('show');
    //     productModal.find('.modal-title').text('Add New Product');
    // });

    $(document).on("click", ".edit-product", function (){
        var tr = $(this).closest('tr');
        $("#id").val(tr.data('id'));
        $("#name").val(tr.data('name'));
        $("#unit").val(tr.data('unit'));
        $("#price").val(tr.data('price'));
        productModel.find('.modal-title').text('Edit Product');
        productModal.modal('show');
    });

    // // Add Product
    // $("#addProduct").on("click", function () {
    //     productModal.modal('show');
    //     productModal.find('.modal-title').text('Add New Product');
    // });

    // // Edit Product
    // $(document).on("click", ".edit-product", function (){
    //     var tr = $(this).closest('tr');
    //     productModal.modal('show');
    //     productModal.find('.modal-title').text('Edit Product');
    //     $("#id").val(tr.data('id'));
    //     $("#name").val(tr.data('name'));
    //     $("#unit").val(tr.data('unit'));
    //     $("#price").val(tr.data('price'));
    // });

    // Submit Product Form
    $("#productForm").on("submit", function (e) {
        e.preventDefault();
        var data = $(this).serializeArray();
        var requestPayload = {
            product_name: null,
            unit_id: null,
            price_per_unit: null
    }});





    // Save Product
    $("#saveProduct").on("click", function () {
        // If we found id value in form then update product detail
        var data = $("#productForm").serializeArray();
        var requestPayload = {
            product_name: null,
            unit_id: null,
            price_per_unit: null
        };
        for (var i=0;i<data.length;++i) {
            var element = data[i];
            switch(element.name) {
                case 'name':
                    requestPayload.product_name = element.value;
                    break;
                case 'unit':
                    requestPayload.unit_id = element.value;
                    break;
                case 'price':
                    requestPayload.price_per_unit = element.value;
                    break;
            }
        }
        callApi("POST", productSaveApiUrl, {
            'data': JSON.stringify(requestPayload)
        });
    });

    $(document).on("click", ".delete-product", function (){
        var tr = $(this).closest('tr');
        var data = {
            product_id : tr.data('id')
        };
        var isDelete = confirm("Are you sure to delete the item: "+ tr.data('name') +"? \nWarning: \nIf this product is already enlisted in an order the product cannot be deleted until the corresponding order is also deleted!");
        if (isDelete) {
            callApi("POST", productDeleteApiUrl, data);
        }
    });

    productModal.on('hide.bs.modal', function(){
        $("#id").val('0');
        $("#name, #unit, #price").val('');
        productModal.find('.modal-title').text('Add New Product');
    });

    productModal.on('show.bs.modal', function(){
        //JSON data by API call
        $.get(unitListApiUrl, function (response) {
            if(response) {
                var options = '<option value="">--Select--</option>';
                $.each(response, function(index, unit) {
                    options += '<option value="'+ unit.unit_id +'">'+ unit.unit_name +'</option>';
                });
                $("#unit").empty().html(options);
            }
        });
    });