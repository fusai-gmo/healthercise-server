<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('activity_list', function (Blueprint $table) {
            $table->id();
            $table->timestamps();
            $table->integer('activityStrength');
            $table->dateTime('activityName');
            $table->integer('activityCalory');

        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('activity_list');
    }
};
