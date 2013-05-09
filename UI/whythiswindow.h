#ifndef WHYTHISWINDOW_H
#define WHYTHISWINDOW_H

#include <QMainWindow>
#include "movielisty1.h"
#include "userproflisty2.h"
#include "displayy3.h"
#include <QStackedWidget>

namespace Ui {
class whythiswindow;
}

class whythiswindow : public QMainWindow
{
    Q_OBJECT
    
public:
    movielisty1 *ml;
    userproflisty2 *upl;
    displayy3 *dis;
    QStackedWidget *stackedwidget;
    explicit whythiswindow(QWidget *parent = 0);
    ~whythiswindow();
    

public slots:

    void movenext();
    void movetwotothree();

private:
    Ui::whythiswindow *ui;
};

#endif // WHYTHISWINDOW_H
