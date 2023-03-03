import browsersync from 'browser-sync';
import sass from 'sass';
import gulpsass from "gulp-sass";
import autoprefixer from 'gulp-autoprefixer';
import rename from 'gulp-rename';
import cleancss from 'gulp-clean-css';


export const modules = {
    browsersync : browsersync,
    sass : gulpsass(sass),
    autoprefixer : autoprefixer,
    rename : rename,
    cleancss : cleancss,
};