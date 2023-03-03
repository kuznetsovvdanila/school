import execute from 'child_process';

export const rundjango = () => {
    execute.exec('python manage.py runserver');
    return new Promise(function(resolve, reject) {
        console.log("HTTP Server Started");
        resolve();
    });
};

export const server = (done) => {
    app.modules.browsersync.init({
        // server: {
        //     baseDir: "school" 
        // },
        notify: false,
        port: 8000,
        proxy: '127.0.0.1:8000'
    });
};