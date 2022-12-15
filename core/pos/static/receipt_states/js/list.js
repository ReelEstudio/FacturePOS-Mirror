var tblReceiptStates;
var input_date_range;
var select_receipts;
var receipt_states = {
    list: function (all) {
        var parameters = {
            'action': 'search',
            'start_date': input_date_range.data('daterangepicker').startDate.format('YYYY-MM-DD'),
            'end_date': input_date_range.data('daterangepicker').endDate.format('YYYY-MM-DD'),
            'receipts': select_receipts.val()
        };
        if (all) {
            parameters['start_date'] = '';
            parameters['end_date'] = '';
        }
        tblReceiptStates = $('#data').DataTable({
            autoWidth: false,
            destroy: true,
            deferRender: true,
            order: [[0, 'desc'], [1, 'asc']],
            ajax: {
                url: pathname,
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: parameters,
                dataSrc: ""
            },
            columns: [
                {data: "datetime_joined"},
                {data: "instance.voucher_number"},
                {data: "instance.receipts.name"},
                {data: "archive"},
                {data: "instance.environment_type.name"},
                {data: "errors"},
                {data: "state"},
                {data: "status.name"},
                {data: "id"},
            ],
            columnDefs: [
                {
                    targets: [-5, -7, -8, -9],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return data;
                    }
                },
                {
                    targets: [-4],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if ($.isEmptyObject(row.errors)) {
                            return 'Sin errores';
                        }
                        return '<a class="btn btn-warning btn-xs" rel="errors"><i class="fas fa-exclamation-triangle"></i></a>';
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        var name = row.status.name;
                        switch (row.status.id) {
                            case "generated":
                                return '<span class="badge badge-info badge-pill">' + name + '</span>';
                            case "signed":
                                return '<span class="badge badge-primary badge-pill">' + name + '</span>';
                            case "valid":
                                return '<span class="badge badge-secondary badge-pill">' + name + '</span>';
                            case "authorized":
                                return '<span class="badge badge-success badge-pill">' + name + '</span>';
                        }
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (data) {
                            return '<span class="badge badge-success badge-pill">Success</span>';
                        }
                        return '<span class="badge badge-danger badge-pill">Error</span>';
                    }
                },
                {
                    targets: [-6],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (!$.isEmptyObject(row.archive)) {
                            return '<a target="_blank" href="' + row.archive + '" class="btn btn-secondary btn-xs btn-flat"><i class="fa-solid fa-file-circle-check"></i></a>';
                        }
                        return '<i class="fa-solid fa-file-circle-minus"></i>';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<a href="' + pathname + 'delete/' + row.id + '/" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash"></i></a>';
                    }
                },
            ],
            rowCallback: function (row, data, index) {

            },
            initComplete: function (settings, json) {
                $(this).wrap('<div class="dataTables_scroll"><div/>');
            }
        });
    },
    formatRow: function (items) {
        // var content = '<div class="card p-3 mt-2"><div class="row"><div class="col-lg-12"><table class="table table-bordered" style="width: 100%;"><thead class="thead-dark"><tr><th style="width: 10%;">Key</th><th style="width: 90%;">Valor</th></tr></thead><tbody>';
        // Object.keys(items.errors).forEach(function (key) {
        //     var item = items.errors[key];
        //     if (typeof item === "object") {
        //         item = JSON.stringify(item);
        //     }
        //     content += '<tr><td>' + key + '</td><td>' + item + '</td></tr>';
        // });
        // content += '</tbody></table></div></div></div>';
        // return content;
        return JSON.stringify(items.errors);
    }
};

$(function () {

    select_receipts = $('select[name="receipts"]');
    input_date_range = $('input[name="date_range"]');

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es"
    });

    input_date_range
        .daterangepicker({
                language: 'auto',
                startDate: new Date(),
                locale: {
                    format: 'YYYY-MM-DD',
                },
                autoApply: true,
            }
        )
        .on('change.daterangepicker apply.daterangepicker', function (ev, picker) {
            receipt_states.list(false);
        });

    $('.drp-buttons').hide();

    receipt_states.list(false);

    $('.btnSearchAll').on('click', function () {
        receipt_states.list(true);
    });

    select_receipts.on('change', function () {
        receipt_states.list(false);
    });

    $('#data tbody')
        .off()
        .on('click', 'a[rel="errors"]', function () {
            var cell = tblReceiptStates.cell($(this).closest('td, li')).index();
            var data = tblReceiptStates.row(cell.row).data();
            var tr = $(this).closest('tr');
            var row = tblReceiptStates.row(tr);
            if (row.child.isShown()) {
                row.child.hide();
                tr.removeClass('shown');
            } else {
                row.child(receipt_states.formatRow(data)).show();
                tr.addClass('shown');
            }
        });
});