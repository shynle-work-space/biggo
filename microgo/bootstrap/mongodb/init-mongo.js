var adminUser = {
    user: 'accessuser',
    pwd: 'accesspwd',
    roles: [
        // {
        //     role: 'readWrite',
        //     db: 'image_records',
        // },
        {
            role: 'readWrite',
            db: 'celery',
        },
        {
            role: 'readWrite',
            db: 'log',
        },

    ],
}

var adminDb = db.getSiblingDB('admin');
adminDb.createUser(adminUser);

// // db.getSiblingDB('admin').auth(adminUser.user, adminUser.pwd);
// imgDb = new Mongo().getDB("image_records");
// imgDb.createCollection('images', { capped: false });

logDb = new Mongo().getDB("log");
logDb.createCollection('logs', { capped: false });