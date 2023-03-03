function HTML() {
    return app.gulp.src(app.path.html.files)
        .pipe(app.modules.browsersync.stream());
};

function SASS() {
    return app.gulp.src(app.path.sass.files, { sourcemaps : true })
        .pipe(app.modules.sass( ))
        .pipe(app.modules.autoprefixer({
            grid : true,
            overrideBrowserslist: ["last 3 versions"],
            cascade: true
            }))
        .pipe(app.modules.rename({
            extname : ".min.css"
        }))
        .pipe(app.modules.cleancss())
        .pipe(app.gulp.dest(app.path.css.dest))
        .pipe(app.modules.browsersync.stream());
};

export function watch() {
    app.gulp.watch(app.path.html.files, HTML);
    app.gulp.watch(app.path.sass.files, SASS);
};