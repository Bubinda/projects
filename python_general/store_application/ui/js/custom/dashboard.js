$(function () {
    //Json data by api call for order table
    $.get(orderListApiUrl, function (response) {
        if(response) {
            var table = '';
            var totalCost = 0;
            $.each(response, function(index, order) {
                totalCost += parseFloat(order.total_cost);
                table += '<tr>' +
                    '<td>'+ order.order_id +'</td>'+    
                    '<td>'+ order.date +'</td>'+
                    '<td>'+ order.customer_id +'</td>'+
                    '<td>'+ order.total_cost.toFixed(2) +' Euro</td></tr>';
            });
            table += '<tr><td colspan="3" style="text-align: end"><b>Total Store Revenue</b></td><td><b>'+ totalCost.toFixed(2) +' Euro</b></td></tr>';
            $("table").find('tbody').empty().html(table);
        }
    });
});