 
let ID_USUARIO = 0;
let passChanged = ''

const listUsers = () => {
    const url = '/listUsers';
    const data = {
        idUser: idUser,
        name: '',
        email: '',
        keep: keep
    };

    const success = function (response) {
        const data = eval(response);
        refreshGrid(['gridUsuario'], data);
    };

    doranAjax(url, data, success);
};

const newUser = () => {
    $('#divFormUser').modal();
    passChanged = '';
    resetaForm();

    setTimeout(() => {
        $('#TXT_USER_NAME').focus();
    }, 500);
};

const resetaForm = () => {
    ID_USUARIO = 0;
    $('#TXT_USER_NAME').val('');
    $('#TXT_EMAIL_USER').val('');
    $('#TXT_PASSWORD1').val('');
    $('#CB_USER_ENABLED').val('1');
    $('#CB_KIND_USER').val('1');
};

const editUser = (_ID_USUARIO) => {
    ID_USUARIO = _ID_USUARIO;

    const url = '/getUser';
    const data = { 
        ID_USER: ID_USUARIO, 
        idUser: idUser,
        keep: keep
    };

    const success = function (response) {
        let data1 = eval(response);
        data1 = eval(data1.message)[0];

        passChanged = data1.PASSWORD1;

        $('#TXT_USER_NAME').val(data1.NAME_USER);
        $('#TXT_EMAIL_USER').val(data1.EMAIL);
        $('#TXT_PASSWORD1').val(data1.PASSWORD1);
        $('#CB_USER_ENABLED').val(data1.USER_ENABLED);
        $('#CB_KIND_USER').val(data1.KIND_OF_USER);

        $('#divFormUser').modal();

        setTimeout(() => {
            $('#TXT_USER_NAME').focus();
        }, 500);
    }

    doranAjax(url, data, success);
};

const saveUser = () => {
    event.preventDefault();

    if ($('#TXT_USER_NAME').val().trim() == ''
        || $('#TXT_EMAIL_USER').val().trim() == ''
        || $('#TXT_PASSWORD1').val().trim() == '') {
        MensagemDeErro('Preencha todos os campos');
        return;
    }

    const url = '/saveUser';

    const data = {
        ID_USER: ID_USUARIO,
        NAME_USER: $('#TXT_USER_NAME').val(),
        EMAIL: $('#TXT_EMAIL_USER').val(),
        PASSWORD1: passChanged != $('#TXT_PASSWORD1').val() ? 
            $('#TXT_PASSWORD1').val() : '',
        USER_ENABLED: $('#CB_USER_ENABLED').val(),
        KIND_OF_USER: $('#CB_KIND_USER').val(),
        idUser: idUser,
        keep: keep
    };

    const success = function (response) {
        if (parseInt(ID_USUARIO) > 0)
            $('#divFormUser').modal('hide');

        resetaForm();

        listUsers();
    };

    doranAjax(url, data, success);
};

const deleteUser = (_ID_USUARIO) => {
    MensagemDeConfirmacao('Deseja deletar o registro?', function () {
        const url = '/deleteUser';

        const data = {
            ID_USER: _ID_USUARIO,
            keep: keep,
            idUser: idUser
        };

        const success = function (response) {
            listUsers();
        }

        doranAjax(url, data, success);
    });
};

const refreshUser = () => {
    event.preventDefault();
    listUsers();
};

const cancelUser = () => {
    event.preventDefault();
    $('#divFormUser').modal('hide');
};
