#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include "firstwindow.h"
#include "upload.h"
#include "userprofile.h"
#include "reducedimension.h"
#include "computesimilarity.h"
#include "clusterusers.h"
#include "recommend.h"

#include <QStackedWidget>


namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT
    
public:
     QStackedWidget *stackedWidget;
    FirstWindow *fw;
    upload *up;
    userprofile *userpro;
    reduceDimension *reducedim;
    computesimilarity *computesimi;
    clusterusers *clusteruser;
    recommend *reco;


    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();
    
private:
    Ui::MainWindow *ui;

public slots:
    void movesecond();
    void moveuserprofile();
    void movereducedim();
    void movetocomputesimilarity();
    void movetoclusteruser();
    void movetorecommend();

    void movebacktoupload();
    void movebacktouserprofile();
    void movebacktoreducedimension();
    void movebacktocomputesimilarity();
    void movebacktoclusterusers();

};

#endif // MAINWINDOW_H
