import gulp from "gulp";
import { path } from './gulp/config/path.js';
import { modules } from  './gulp/config/plugins.js';

global.app = {
    path : path,
    gulp : gulp,
    modules : modules,
};

//import { log } from './gulp/tasks/sass.js';
import { watch } from "./gulp/tasks/watcher.js";
import { server, rundjango } from "./gulp/tasks/server.js"

gulp.task('runserver', rundjango);

const task1 = gulp.parallel(gulp.series('runserver', server), watch);

gulp.task('default', task1);