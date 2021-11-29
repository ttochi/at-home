function listPickupMobility(admin, callback) {
  // check admin authentication
  if(!admin.validate)
    throw new Error('No Authorization');

  // run pickup list algorithm
  callback(admin.getCurrentPosition());
}

listPickupMobility(adminA, algorithmA);
listPickupMobility(adminB, algorithmB);
